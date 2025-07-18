import sys
import json
import itertools

from checkbox_submission_tools import utils


def add_parser(subparser):
    parser_journal = subparser.add_parser(
        "journalctl", help="Print a readable Journalctl output from submission"
    )
    parser_journal.set_defaults(func=get_journal_text)
    parser_journal.add_argument("submission_json_path")
    parser_journal.add_argument(
        "identifier_match",
        help="Filter output to only matching unit/identifiers",
        nargs="*",
    )
    parser_journal.add_argument(
        "--only-job",
        help="Best effort filter to extract logs of a job id",
    )


def add_date_field(journal_entry: dict):
    if journal_entry.get("__REALTIME_TIMESTAMP"):
        timestamp_microseconds = int(journal_entry["__REALTIME_TIMESTAMP"])
        journal_entry["HUMAN_TIMESTAMP"] = utils.realtime_to_humantime(
            timestamp_microseconds
        )
    return journal_entry


def find_start_job(journal_dicts: list[dict], job_id: str):
    journal_dicts = iter(journal_dicts)
    for entry in journal_dicts:
        if "checkbox" not in entry.get("_SYSTEMD_UNIT", ""):
            continue
        if "INFO:plainbox.unified:Running" not in entry.get("MESSAGE", ""):
            continue
        if job_id not in entry["MESSAGE"]:
            continue
        return itertools.chain([entry], journal_dicts)
    raise SystemExit(f"Job '{job_id}' is not in the logs!")


def till_end_of_job(journal_dicts: list[dict]):
    for x in journal_dicts:
        if "checkbox" not in x.get("_SYSTEMD_UNIT", ""):
            yield x
        elif "INFO:plainbox.session.state" not in x.get("MESSAGE", ""):
            yield x
        # this can be MemoryJobResult, DiskJobResult etc.
        elif "JobResult" not in x["MESSAGE"]:
            yield x
        else:
            yield x
            return


def get_journal_text(args):
    submission_path = args.submission_json_path
    formatters = [
        "[{__MONOTONIC_TIMESTAMP}][{HUMAN_TIMESTAMP}][{_SYSTEMD_UNIT}]: {MESSAGE}\n",
        "[{__MONOTONIC_TIMESTAMP}][{HUMAN_TIMESTAMP}][{SYSLOG_IDENTIFIER}]: {MESSAGE}\n",
        "[{__MONOTONIC_TIMESTAMP}][{HUMAN_TIMESTAMP}][{GLIB_DOMAIN}]: {MESSAGE}\n",
        "[{__MONOTONIC_TIMESTAMP}][{HUMAN_TIMESTAMP}][pid: {_PID} gid: {_GID}]: {MESSAGE}\n",
        "[{__MONOTONIC_TIMESTAMP}][{HUMAN_TIMESTAMP}][???]: {MESSAGE}\n",
    ]
    with open(submission_path) as f:
        submission_json = json.load(f)
    try:
        journal_out = submission_json["system_information"]["journalctl"]
    except KeyError:
        raise SystemExit(
            "Submission is too old, no system information journalctl found"
        )
    if not journal_out["success"]:
        raise SystemExit("Journalctl failed to collect in this submission")
    journal_out = journal_out["outputs"]["payload"]

    journal_human_dated = map(add_date_field, journal_out)

    if args.only_job:
        journal_human_dated = find_start_job(
            journal_human_dated, args.only_job
        )
        journal_human_dated = till_end_of_job(journal_human_dated)

    journal_repr_iter = map(
        utils.fallback_formatter(formatters), journal_human_dated
    )
    sys.stdout.writelines(journal_repr_iter)
