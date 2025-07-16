import sys
import argparse

from checkbox_submission_tools import (
    get_ids,
    journalctl,
    get_devices,
    get_submission_json,
)


def parse_args(argv):
    parser = argparse.ArgumentParser("Checkbox submission tools")
    sp = parser.add_subparsers(help="actions", dest="subparser", required=True)
    journalctl.add_parser(sp)
    get_ids.add_parser(sp)
    get_devices.add_parser(sp)
    get_submission_json.add_parser(sp)
    return parser.parse_args(argv)


def main():
    args = parse_args(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
