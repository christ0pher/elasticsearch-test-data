from collections import OrderedDict
import json
import tornado.options

__author__ = 'christopher@levire.com'


def create_format_from_index(index_file, index_type):
    with open(index_file) as index:
        parsed_index = json.load(index)

    index_properties = OrderedDict(sorted(parsed_index["mappings"][index_type]["properties"].items()))

    return create_format(index_properties, "")


def create_format(index_properties, result_format, type_delimiter=":", property_delimiter=","):
    for property_name, property_content in index_properties.items():
        property_type = index_properties[property_name]["type"]
        if property_type == "string":
            result_format += property_name + type_delimiter + "str" + property_delimiter
        elif property_type == "integer":
            result_format += property_name + type_delimiter + "int" + property_delimiter
        elif property_type == "float":
            pass
        elif property_type == "nested":
            result_format += property_name + type_delimiter + "no" + type_delimiter + create_format(property_content["properties"], "", type_delimiter=";", property_delimiter="-") + property_delimiter
    return result_format[:-1]  # remove the last comma.


if __name__ == '__main__':
    tornado.options.define("index_file", type=str, default='index.json', help="Path to the index-definition file")
    tornado.options.define("index_type", type=str, default='type', help="Index-type")

    tornado.options.parse_command_line()

    format = create_format_from_index(tornado.options.options.index_file, tornado.options.options.index_type)

    print(format)