import sys
import json
from itertools import chain


def add_parser(subparser):
    parser = subparser.add_parser(
        "get_ids", help="Extracts ids from a submission"
    )
    parser.set_defaults(func=get_ids)
    parser.add_argument("submission_json_path")


def get_ids(args):
    submission_path = args.submission_json_path
    with open(submission_path) as f:
        submission_json = json.load(f)

    def get_printable_id(x):
        if "full_id" not in x:
            breakpoint()
        return x["full_id"] + "\n"

    to_print = submission_json["results"]
    to_print = chain(to_print, submission_json.get("rejected-jobs", []))
    to_print = chain(to_print, submission_json.get("resource-results", []))
    to_print = chain(to_print, submission_json.get("attachment-results", []))

    to_print = map(get_printable_id, to_print)

    sys.stdout.writelines(to_print)
