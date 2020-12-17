import copy
import functools
import re
import sys

from .exceptions.exception_handler import BadObjectType


def parse_object_type(object_types, object_type):
    if object_type is None or object_type == "":
        return None
    try:
        _obj = object_type.lower()
    except AttributeError:
        raise BadObjectType(object_types, object_type)

    if re.match(r"^flask.*$", _obj):
        obj = object_types[0]["name"]
    elif re.match(r"^gem.*$", _obj):
        obj = object_types[1]["name"]
    else:
        raise BadObjectType(object_types, object_type)

    return obj


def filter_object_type(object_type, stashes):
    # The base object can't be iterated over while beeing modified
    temp_stashes = copy.deepcopy(stashes)
    i = 0
    object_type += "s"
    # Remove unwanted type
    for stash in temp_stashes:
        for k, v in stash["items"].items():
            if object_type not in k:
                del stashes[i]["items"][k]
        i += 1
    # Remove empty stash
    i = 0
    for stash in stashes:
        if len(stash["items"].get(object_type, [])) == 0:
            del stashes[i]
        i += 1
    return stashes


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


def print_stash_result(obj_type, limit, stashes):
    r = ""
    gem_result = "".join(
        [
            f"\nStash tab `{stash['name']}`, number {stash['id'] + 1}:\n"
            f"For {sum(stash['items']['gems']) / limit} potential compos,\n"
            f"{stash['results']['gems_result']['currencies']} Gemcutter's Prisms "
            "can be really obtained\n"
            f"Batches are:\n{stash['results']['gems_result']['result']}\n"
            "Remaining items are:\n"
            f"{compute_values_from_indexes(stash['items']['gems'], stash['results']['gems_result']['remaining'])}\n"  # noqa: E501
            for stash in stashes
            if stash["results"].get("gems_result", False)
        ]
    )
    flask_result = "".join(
        [
            f"\nStash tab `{stash['name']}`, number {stash['id'] + 1}:\n"
            f"For {sum(stash['items']['flasks']) / limit} potential compos,\n"
            f"{stash['results']['flasks_result']['currencies']} Glassblower's Baubles "
            "can be really obtained\n"
            f"Batches are:\n{stash['results']['flasks_result']['result']}\n"
            "Remaining items are:\n"
            f"{compute_values_from_indexes(stash['items']['flasks'], stash['results']['flasks_result']['remaining'])}\n"  # noqa: E501
            for stash in stashes
            if stash["results"].get("flasks_result", False)
        ]
    )
    r += "\n\n" + 30 * "-" + "\nGEMS RESULT\n\n"
    r += gem_result
    r += "\n\n" + 30 * "-" + "\nFLASKS RESULT\n\n"
    r += flask_result
    r += "\n\n" + 30 * "-" + "\n\n"
    return r
