from collections import OrderedDict
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


class TestNestedFormatCreation(TestCase):

    def setUp(self):
        with open("testindex.json", "w+") as indexfile:
            index = OrderedDict({
                "template" : "test*",
                "mappings" : OrderedDict({
                    "properties":
                        {
                            "test_int_field" : {"type": "integer"},
                            "test_string_field" : {"type": "string"},
                            "test_nested_field" : OrderedDict({
                                "type": "nested",
                                "properties": OrderedDict([
                                    ("test_ns_int_field" , {"type": "integer"}),
                                    ("test_ns_string_field" , {"type": "string"})
                                ])
                            })
                        }
                })
            })
            json.dump(index, indexfile)

    def tearDown(self):
        os.remove("testindex.json")


    def test_convert_easy_index(self):

        format = create_format_from_index("testindex.json")

        self.assertEqual(format, "test_int_field:int,test_nested_field:no:test_ns_int_field;int-test_ns_string_field;str,test_string_field:str")