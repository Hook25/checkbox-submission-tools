import sys
import argparse

from checkbox_submission_tools.journalctl import get_journal_text


def parse_args(argv):
    parser = argparse.ArgumentParser("Checkbox submission tools")
    sp = parser.add_subparsers(help="actions", dest="subparser", required=True)
    parser_journal = sp.add_parser(
        "journalctl", help="Journalctl extraction utility"
    )
    parser_journal.set_defaults(func=get_journal_text)
    parser_journal.add_argument("submission_json_path")
    return parser.parse_args(argv)


def main():
    args = parse_args(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
