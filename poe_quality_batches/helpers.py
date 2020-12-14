import re

from .exceptions.exception_handler import BadObjectType


def parse_object_type(object_types, _object):
    try:
        _obj = _object.lower()
    except AttributeError:
        raise BadObjectType(object_types, _object)

    if re.match(r"^flask.*$", _obj):
        obj = object_types[0]["id"]
    elif re.match(r"^gem.*$", _obj):
        obj = object_types[1]["id"]
    else:
        raise BadObjectType(object_types, _object)

    return obj


def is_there_missing_vars():
    raise NotImplementedError()


def find_uniques(items: list) -> list:
    uniques = list()
    temp = list()
    for i in range(len(items)):
        if items[i] not in temp:
            uniques.append(tuple((i, items[i])))
            temp.append(items[i])
    return uniques


def compute_values_from_indexes(items: list, rem: list) -> list:
    # Debug method
    rem_items = [items[x] for x in rem]
    return rem_items
