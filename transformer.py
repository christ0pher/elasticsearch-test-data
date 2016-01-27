from collections import OrderedDict
import json
import tornado.options

__author__ = 'christopher@levire.com'


def create_format_from_index(index_file):
    with open(index_file) as index:
        parsed_index = json.load(index)

    index_properties = OrderedDict(sorted(parsed_index["mappings"]["properties"].items()))

    result_format = ""

    for property_name, property_content in index_properties.items():
        property_type = index_properties[property_name]["type"]
        if property_type == "string":
            result_format += property_name+":str,"
        elif property_type == "integer":
            result_format += property_name+":int,"
        elif property_type == "float":
            pass
        elif property_type == "nested":
            pass

    return result_format[:-1] # remove the last comma.



if __name__ == '__main__':
    tornado.options.define("index_file", type=str, default='index.json', help="Path to the index-definition file")

    tornado.options.parse_command_line()

    format = create_format_from_index(tornado.options.options.index_file)