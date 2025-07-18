import sys
import json

from checkbox_submission_tools import utils


def add_parser(subparser):
    parser = subparser.add_parser(
        "get_devices", help="Extracts ids from a submission"
    )
    parser.set_defaults(func=get_devices)
    parser.add_argument("--only-categorized", action="store_true")
    parser.add_argument("submission_json_path")


def get_devices(args):
    submission_path = args.submission_json_path
    with open(submission_path) as f:
        submission_json = json.load(f)

    devices = submission_json["devices"]

    if args.only_categorized:
        devices = filter(lambda x: "category" in x, devices)

    formatter = utils.fallback_formatter(
        [
            "{bus} ({category}): {driver} -> {product}\n",
            "{bus} ({category}): -> {product}\n",
            "{bus} ({category}): -> {name}\n",
            "{bus}: {driver} -> {product}\n",
            "{bus}: {driver} -> {vendor}\n",
            "{bus}: {vendor}\n",
            "{bus}: {driver}\n",
        ]
    )
    to_print = map(formatter, devices)

    sys.stdout.writelines(to_print)
