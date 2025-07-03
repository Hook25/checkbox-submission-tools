import sys
import json

from checkbox_submission_tools import utils


def add_parser(subparser):
    parser = subparser.add_parser(
        "get_devices", help="Extracts ids from a submission"
    )
    parser.set_defaults(func=get_devices)
    parser.add_argument("submission_json_path")


def get_devices(args):
    submission_path = args.submission_json_path
    with open(submission_path) as f:
        submission_json = json.load(f)

    formatter = utils.fallback_formatter(
        [
            "{bus} ({category}): {driver} -> {product}\n",
            "{bus} ({category}): -> {product}\n",
            "{bus}: {driver} -> {product}\n",
            "{bus}: {driver} -> {vendor}\n",
            "{bus}: {vendor}\n",
            "{bus}: {driver}\n",
        ]
    )
    to_print = map(formatter, submission_json["devices"])

    sys.stdout.writelines(to_print)
