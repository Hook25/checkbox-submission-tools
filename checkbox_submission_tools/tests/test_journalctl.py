from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from checkbox_submission_tools import journalctl


class TestGetJournalText(TestCase):
    @patch("checkbox_submission_tools.journalctl.open", new=MagicMock())
    @patch("sys.stdout.writelines")
    @patch("json.load")
    def test_normal_messages(
        self, json_load_mock: Mock, stdout_writelines_mock: Mock
    ):
        json_load_mock.return_value = {
            "system_information": {
                "journalctl": {
                    "success": True,
                    "outputs": {
                        "payload": [
                            {
                                "__MONOTONIC_TIMESTAMP": 0,
                                "_SYSTEMD_UNIT": "checkbox-ng.service",
                                "MESSAGE": "painbox fun",
                            }
                        ]
                    },
                }
            }
        }
        journalctl.get_journal_text(Mock(only_job=None))
        stdout_writelines_mock.assert_called()

    @patch("checkbox_submission_tools.journalctl.open", new=MagicMock())
    @patch("sys.stdout.writelines")
    @patch("json.load")
    def test_kernel_messages(
        self, json_load_mock: Mock, stdout_writelines_mock: Mock
    ):
        json_load_mock.return_value = {
            "system_information": {
                "journalctl": {
                    "success": True,
                    "outputs": {
                        "payload": [
                            {
                                "__MONOTONIC_TIMESTAMP": 0,
                                "SYSLOG_IDENTIFIER": "kernel",
                                "MESSAGE": "painbox fun",
                            }
                        ]
                    },
                }
            }
        }
        journalctl.get_journal_text(Mock(only_job=None))
        stdout_writelines_mock.assert_called()
