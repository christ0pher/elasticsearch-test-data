from unittest import TestCase
from parser.format_parser import get_data_for_format

__author__ = 'christopher@levire.com'


class TestParseFormat(TestCase):

    def test_parse_nested_object_format(self):

        format = "nested_object:no:my_integer;int-my_string;str"

        result_name, result_data = get_data_for_format(format)

        self.assertEqual(type(result_data), list)
        self.assertEqual(len(result_data), 1)
        self.assertEqual(result_name, "nested_object")

