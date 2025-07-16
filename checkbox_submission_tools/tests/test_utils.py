from unittest import TestCase

from checkbox_submission_tools.utils import realtime_to_humantime


class TestRealtimeToHumantime(TestCase):
    def test_conversion_ok(self):
        assert realtime_to_humantime(1745680453048679) == "2025-04-26 15:14:13 UTC"
