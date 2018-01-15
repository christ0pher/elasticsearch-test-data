from value_generator.default_value_generator import create_value_from_dict, get_word_from_wordlist, \
    create_random_timestamp, create_random_int, create_random_string

__author__ = 'christopher@levire.com'


def get_data_for_format(format, splitter=":"):
    split_f = format.split(splitter)
    if not split_f:
        return None, None

    field_name = split_f[0]
    field_type = split_f[1]

    if field_type == "str":
        return_val = create_random_string(split_f)

    elif field_type == "int":
        return_val = create_random_int(split_f)

    elif field_type == "ts":
        return_val = create_random_timestamp(split_f)

    elif field_type == "words":
        return_val = get_word_from_wordlist(split_f)

    elif field_type == "dict":
        dict_name=split_f[2]
        return_val = create_value_from_dict(split_f, dict_name)

    elif field_type == "no": # nested object
        nested_object_format = split_f[2].split("-")
        return_val = {}
        for format in nested_object_format:
            field, value = get_data_for_format(format, splitter=";")
            return_val[field] = value
        return_val = [return_val]

    return field_name, return_val