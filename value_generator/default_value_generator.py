import random
import string
import time

__author__ = 'christopher@levire.com'

DICT_DATA = []


def set_dict_data(data):
    global DICT_DATA
    DICT_DATA = data


def create_value_from_dict(split_f, dict_name):
    global DICT_DATA
    min = 2 if len(split_f) < 4 else int(split_f[3])
    max = min + 8 if len(split_f) < 5 else int(split_f[4])
    if max - min == 0:
        count = min
    else:
        count = random.randrange(min, max)
    word_dict = DICT_DATA[dict_name]
    return_val = " ".join([random.choice(word_dict).strip() for _ in range(count)])
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