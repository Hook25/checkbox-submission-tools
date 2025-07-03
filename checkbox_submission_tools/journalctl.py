import sys
import json
from contextlib import suppress
from functools import partial


def add_parser(subparser):
    parser_journal = subparser.add_parser(
        "journalctl", help="Print a readable Journalctl output from submission"
    )
    parser_journal.set_defaults(func=get_journal_text)
    parser_journal.add_argument("submission_json_path")


def fallback_formatter(formatters: list[str]):
    def _f(x: dict):
        formatters_i = iter(formatters)
        while True:
            with suppress(KeyError):
                return next(formatters_i).format(**x)

    return _f


def get_journal_text(args):
    submission_path = args.submission_json_path
    formatters = [
        "[{__MONOTONIC_TIMESTAMP}][{_SYSTEMD_UNIT}]: {MESSAGE}\n",
        "[{__MONOTONIC_TIMESTAMP}][{SYSLOG_IDENTIFIER}]: {MESSAGE}\n",
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

    journal_repr_iter = map((fallback_formatter(formatters)), journal_out)
    sys.stdout.writelines(journal_repr_iter)
