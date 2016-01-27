import random
import string
import time

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
        return_val = create_value_from_dict(split_f)

    elif field_type == "no": # nested object
        nested_object_format = split_f[2].split("-")
        return_val = {}
        for format in nested_object_format:
            field, value = get_data_for_format(format, splitter=";")
            return_val[field] = value

    return field_name, return_val


def create_value_from_dict(split_f):
    global _dict_data
    min = 2 if len(split_f) < 3 else int(split_f[2])
    max = min + 8 if len(split_f) < 4 else int(split_f[3])
    count = random.randrange(min, max)
    return_val = " ".join([random.choice(_dict_data).strip() for _ in range(count)])
    return return_val


def get_word_from_wordlist(split_f):
    min = 2 if len(split_f) < 3 else int(split_f[2])
    max = min + 8 if len(split_f) < 4 else int(split_f[3])
    count = random.randrange(min, max)
    words = []
    for _ in range(count):
        word_len = random.randrange(3, 10)
        words.append("".join([random.choice(string.ascii_letters + string.digits) for x in range(word_len)]))
    return_val = " ".join(words)
    return return_val


def create_random_timestamp(split_f):
    now = int(time.time())
    per_day = 24 * 60 * 60
    min = now - 30 * per_day if len(split_f) < 3 else int(split_f[2])
    max = now + 30 * per_day if len(split_f) < 4 else int(split_f[3])
    return_val = int(random.randrange(min, max) * 1000)
    return return_val


def create_random_int(split_f):
    min = 0 if len(split_f) < 3 else int(split_f[2])
    max = min + 100000 if len(split_f) < 4 else int(split_f[3])
    return_val = random.randrange(min, max)
    return return_val


def create_random_string(split_f):
    min = 3 if len(split_f) < 3 else int(split_f[2])
    max = min + 7 if len(split_f) < 4 else int(split_f[3])
    length = random.randrange(min, max)
    return_val = "".join([random.choice(string.ascii_letters + string.digits) for x in range(length)])
    return return_val