from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from checkbox_submission_tools import get_ids


class TestGetJournalText(TestCase):
    @patch("checkbox_submission_tools.journalctl.open", new=MagicMock())
    @patch("sys.stdout.writelines")
    @patch("json.load")
    def test_get_ids_nominal(
        self, json_load_mock: Mock, writelines_mock: Mock
    ):
        json_load_mock.return_value = {
            "results": [{"full_id": "com.canonical.certification::results"}],
            "rejected-jobs": [
                {"full_id": "com.canonical.certification::rejected"}
            ],
            "resource-results": [
                {"full_id": "com.canonical.certification::resource"}
            ],
            "attachment-results": [
                {"full_id": "com.canonical.certification::attachment"}
            ],
        }

        get_ids.get_ids(MagicMock())

        writelines_mock.assert_called()
