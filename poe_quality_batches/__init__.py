"""Initialization of main package
Description
-----------

This script aims to compute the highest number of batch of 40 that can be obtained by
combining the values (integers) stored in a list.

Todo
----
* Features
  * Gather inventory from official website
  * Run a local web interface to easily interact with the tool
* Project
  * Implement Unit Tests
* Script
  * Simplify the win conditon
  * Ensure every available combination is tested
  * Ensure one combination is tested only once"""
import sys

from .core.runner import runner
from .exceptions.exception_handler import BadInput
from .helpers import is_there_missing_vars, find_uniques, compute_values_from_indexes
from .http.client import client


def main(
    account: str,
    realm: str,
    league: str,
    character: str,
    tab_index: str,
    poesessid: str,
    object_type: int,
    force_object_type: bool,
    stash_name: int,
    online: bool,
    limit: int,
    debug: bool,
    strict=False,
):
    if strict is True:
        missing_vars = is_there_missing_vars()
        if missing_vars is not None:
            raise BadInput(missing_vars)
    if online is True:
        from settings.settings import TARGET, ENDPOINT

        url = TARGET + ENDPOINT
        sample_data = client(
            url,
            account,
            realm,
            league,
            character,
            tab_index,
            poesessid,
            object_type,
            force_object_type,
            stash_name,
        )
        sample = sample_data[0]
    else:
        from settings.settings import SAMPLES

        sample = SAMPLES["items_quality"]

    items = sample
    items_len = len(items)
    items = sorted(items, reverse=True)

    # 'uniques' is a list of tuples, where each tuple equal the index of the first
    # occurence of a value, and the value corresponding to this index. It helps to
    # reduce the number of time the recursive method is run.
    uniques = find_uniques(items)

    sys.setrecursionlimit(6000)
    original_stdout = sys.stdout

    # If the debug is enabled, it increase a lot the execution time. It is faster to
    # print in this case in a file rather than in the stdout.
    if debug is True:
        # Block: file out.txt
        with open("out.txt", "w") as f:
            sys.stdout = f
            res, remaining = runner(limit, items, items_len, uniques, debug)
            print(f"For {sum(items) / limit} potential compos,")
            print(
                f"\n{len(res)} compos can be really obtained\nBatches are:\n{res}"
                f"Remaining items are:\n{compute_values_from_indexes(items, remaining)}"
            )
            sys.stdout = original_stdout
    else:
        res, remaining = runner(limit, items, items_len, uniques, debug)
        print(f"For {sum(items) / limit} potential compos,\n")
        print(
            f"{len(res)} compos can be really obtained\nBatches are:\n{res}\n"
            f"Remaining items are:\n{compute_values_from_indexes(items, remaining)}"
        )
