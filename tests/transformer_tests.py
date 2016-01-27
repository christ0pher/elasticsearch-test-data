import json
import os
from unittest import TestCase
from transformer import create_format_from_index

__author__ = 'christopher@levire.com'


class TestFormatCreation(TestCase):

    def setUp(self):
        with open("testindex.json", "w+") as indexfile:
            index = {
                "template" : "test*",
                "mappings" : {
                    "properties":
                        {
                            "test_int_field" : {"type": "integer"},
                            "test_string_field" : {"type": "string"}
                        }
                }
            }
            json.dump(index, indexfile)

    def tearDown(self):
        os.remove("testindex.json")


    def test_convert_easy_index(self):

        format = create_format_from_index("testindex.json")

        self.assertEqual(format, "test_int_field:int,test_string_field:str")