from collections import Mapping
import string
import re


def merge_dicts(original_dict, dict_to_merge):
    for key, value in dict_to_merge.items():
        if isinstance(value, Mapping):
            r = merge_dicts(original_dict.get(key, {}), value)
            original_dict[key] = r
        else:
            original_dict[key] = dict_to_merge[key]
    return original_dict


def find_final_value(keys, data):
    for key in keys:
        if not data:
            return keys, None
        elif isinstance(data, list):
            index_value = int(key)
            if index_value >= len(data):
                data = None
                break
            data = [None if i != index_value else data[i] for i in range(index_value + 1)]
            keys.pop()
            break
        elif '.' in key:
            keys.pop()
            break
        elif isinstance(data, dict):
            data = data.get(key, None)
    return keys, data


def split_string_on_keys(string_):
    p = re.compile('[^\[]\w+|\d+')
    keys = p.findall(string_)
    return keys


def optimize_data(template, data):
    pieces = string.Formatter().parse(template)
    dicts = []

    for piece in pieces:
        field_name = piece[1]
        if not field_name:
            continue

        keys = split_string_on_keys(field_name)
        keys, value = find_final_value(keys, data)

        if not value:
            print('Cannot find value with such template!')
            return

        deepest_depth = {keys[-1]: value}
        for i in range(len(keys)-2, -1, -1):
            deepest_depth = {keys[i]: deepest_depth}

        dicts.append(deepest_depth)

    for i in range(1, len(dicts)):
        dicts[i] = merge_dicts(dicts[i], dicts[i-1])

    if dicts:
        return dicts[-1]
    print('Template format should be like this: "Some text: {some_dict[text]}"')
