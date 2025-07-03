import sys
import json
from itertools import chain

"""
get_ids(){
  cat $1 | jq -r '[.results.[].full_id] + [."rejected-jobs".[].full_id] + [."resource-results".[].full_id] + [."attachment-results".[].full_id]' | jq -r '.[]' | sort | uniq > ids_$1;
}
"""


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
        return x["full_id"] + "\n"

    to_print = map(get_printable_id, submission_json["results"])
    to_print = chain(
        to_print, map(get_printable_id, submission_json["rejected-jobs"])
    )
    to_print = chain(
        to_print, map(get_printable_id, submission_json["resource-results"])
    )
    to_print = chain(
        to_print, map(get_printable_id, submission_json["attachment-results"])
    )

    sys.stdout.writelines(to_print)
