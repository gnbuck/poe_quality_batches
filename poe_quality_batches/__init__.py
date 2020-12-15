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
  * Refactor HTTP module to oriented object style
* Script
  * Simplify the win conditon
  * Ensure every available combination is tested
  * Ensure one combination is tested only once"""
import sys

from .core.runner import runner
from .exceptions.exception_handler import BadInput
from .helpers import (
    compute_values_from_indexes,
    do_debug,
    find_missing_vars,
    find_uniques,
    print_stash_result,
)
from .http.client import Client


def main(
    account: str,
    realm: str,
    league: str,
    character: str,
    poesessid: str,
    object_type: int,
    stash_name: int,
    online: bool,
    limit: int,
    debug: bool,
):
    """Main function."""

    missing_vars = find_missing_vars(account, realm, league, character, poesessid)
    if missing_vars is True:
        raise BadInput(missing_vars)

    if online is True:
        from settings.settings import TARGET, ENDPOINT
        url = TARGET + ENDPOINT
        sample_data = Client(
            url,
            account,
            realm,
            league,
            character,
            poesessid,
            object_type,
            stash_name,
        ).get_content()
        sample = sample_data
    else:
        from settings.samples import SAMPLES
        if debug is True:
            sample = SAMPLES[1:2]
        else:
            sample = SAMPLES

    sys.setrecursionlimit(10000)

    for stash in sample:

        gems_in_stash = stash["items"].get("gems", None)
        if gems_in_stash is not None:
            gem_result = run(gems_in_stash, limit, debug)
            stash["results"]["gems_result"] = gem_result

        flasks_in_stash = stash["items"].get("flasks", None)
        if flasks_in_stash is not None:
            flask_result = run(flasks_in_stash, limit, debug)
            stash["results"]["flasks_result"] = flask_result


@do_debug
def run(items, limit, debug):
    """Wrapper for Runner module."""

    print(items)
    items_len = len(items)
    items = sorted(items, reverse=True)

    # 'uniques' is a list of tuples, where each tuple equal the index of the first
    # occurence of a value, and the value corresponding to this index. It helps to
    # reduce the number of time the recursive method is run.
    uniques = find_uniques(items)
    res, remaining = runner(items, items_len, uniques, limit, debug)

    print_stash_result(items, limit, res, remaining, debug)
    stash_result = {
        "result": res,
        "remaining": remaining,
    }
    print(f"\nstash_result = {stash_result}\n")
    return stash_result
