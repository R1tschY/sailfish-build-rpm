import unittest
from unittest.mock import patch

from action import command

COMMAND_TESTS = [
    ("None command",
     "::missing.command::",
     (None, None, None)),

    ("Simple command",
     "::cmd::",
     ("cmd", None, None)),

    ("Command with value",
     "::cmd::value",
     ("cmd", None, "value")),

    ("Command with parameter",
     "::cmd param=arg::value",
     ("cmd", {"param": "arg"}, "value")),

    ("Command with parameters",
     "::cmd param1=arg1,param2=arg2::value",
     ("cmd", {"param1": "arg1", "param2": "arg2"}, "value")),

    ("Command with non-string parameters and value",
     "::cmd none=,dict={\"test\"%3A\"me\"},bool=true::{\"test\":\"me\"}",
     ("cmd", {"none": None, "dict": {"test": "me"}, "bool": True}, {"test": "me"})),

    ("Escape parameters",
     "::cmd param=percent %25 %25 nl %0A %0A cr %0D %0D comma %2C %2C colon %3A %3A::",
     ("cmd", {"param": "percent % % nl \n \n cr \r \r comma , , colon : :"}, None)),

    ("Escape value",
     "::cmd::percent %25 %25 nl %0A %0A cr %0D %0D",
     ("cmd", None, "percent % % nl \n \n cr \r \r")),
]


class ActionTest(unittest.TestCase):

    @patch('builtins.print')
    def test_commands(self, mock_print):
        for (name, expected, args) in COMMAND_TESTS:
            with self.subTest(msg=name, args=args):
                command(*args)
                mock_print.assert_called_once_with(expected, flush=True)
                mock_print.reset_mock()
