import functools
import re
import sys

from .exceptions.exception_handler import BadObjectType


def parse_object_type(object_types, object_type):
    if object_type is None:
        return -1
    try:
        _obj = object_type.lower()
    except AttributeError:
        raise BadObjectType(object_types, object_type)

    if re.match(r"^flask.*$", _obj):
        obj = object_types[0]["id"]
    elif re.match(r"^gem.*$", _obj):
        obj = object_types[1]["id"]
    else:
        raise BadObjectType(object_types, object_type)

    return obj


def find_missing_vars(*args):
    missing_vars = []
    for arg in args:
        if arg is None:
            missing_vars.append(arg)
    return missing_vars


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


def do_debug(func):
    @functools.wraps(func)
    def wrapper(*args):
        debug = args[-1]
        if debug is True:
            # Block: file out.txt
            original_stdout = sys.stdout
            with open("out.txt", "w") as f:
                sys.stdout = f
                return func(*args)
            sys.stdout = original_stdout
        else:
            return func(*args)

    return wrapper


def print_stash_result(items, limit, res, remaining):
    print(f"For {sum(items) / limit} potential compos,\n")
    print(
        f"{len(res)} compos can be really obtained\nBatches are:\n{res}\n"
        f"Remaining items are:\n{compute_values_from_indexes(items, remaining)}"
    )
