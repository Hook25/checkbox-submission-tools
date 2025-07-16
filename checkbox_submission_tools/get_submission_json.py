import os
import json
import urllib.request


def add_parser(subparser):
    parser = subparser.add_parser(
        "get_submission_json",
        help="Downloads the submission.json for the given submission id",
    )
    parser.set_defaults(func=get_submission_json)
    parser.add_argument("submission_id")
    parser.add_argument(
        "--pretty", help="Format json output", action="store_true"
    )


def to_std_id(submission_id):
    # user may have provided the url, not the plain id
    if "https" not in submission_id:
        return submission_id

    to_r = submission_id.rstrip("/").split("/")[-1]
    print(f"Parsed URL, estimated ID: {to_r}")
    return to_r


def get_submission_json(args):
    """
    Get the validation results of a given list of submissions from the C3 API.
    """
    submission_id = to_std_id(args.submission_id)
    access_token = os.getenv("C3_TOKEN")
    if not access_token:
        raise SystemExit("Export your access token in C3_TOKEN")
    api_url = f"https://certification.canonical.com/api/v2/reports/summary/{submission_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    # Convert the payload to a JSON string
    # Create the request object with the data and headers
    req = urllib.request.Request(api_url, headers=headers, method="GET")
    # Send the request and get the response
    with urllib.request.urlopen(req) as response:
        to_print = response.read().decode("utf-8")
        if args.pretty:
            to_print = json.dumps(json.loads(to_print), indent=4)
        print(to_print)
