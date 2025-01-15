import unittest
from bettercli.command import Command
from bettercli.option import Option, InvalidType, InvalidLength

class TestCommand(unittest.TestCase):
    def setUp(self):
        self.cmd = Command("test")

    def test_validate_command_name(self):
        self.assertTrue(self.cmd.validate(["test"]))
        self.assertFalse(self.cmd.validate(["wrong"]))

    def test_add_positional_option(self):
        self.cmd.add_positional_option("pos", str, "default", length=1)
        self.assertIn("pos", self.cmd.options)
        self.assertIn("pos", self.cmd.pos_options)

    def test_add_keyword_option(self):
        self.cmd.add_keyword_option("kw", str, "default", "-k", "--key", length=1)
        self.assertIn("kw", self.cmd.options)
        self.assertIn("kw", self.cmd.kw_options)
        self.assertTrue(self.cmd.validate(["test", "-k", "kwarg"]))

    def test_run_with_invalid_type(self):
        self.cmd.add_positional_option("num", int, 0, length=1)
        self.cmd.run(["test", "not_a_number"])


    def test_schema(self):
        self.cmd.add_positional_option("pos", str, "default", length=1)
        self.cmd.add_keyword_option("kw", str, "default", "-k", length=1)
        self.assertEqual(self.cmd.schema, ["test", "pos", "kw"])

if __name__ == '__main__':
    unittest.main()
