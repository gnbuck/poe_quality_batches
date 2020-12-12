import sys

from .core.runner import runner
from .helpers import find_uniques
from .http.client import client
from .samples import SAMPLES
from .settings import LIMIT as limit


def main(online, debug):
    if online is True:
        sample = client()
    else:
        sample = SAMPLES["items_quality"]

    items = sample
    items_len = len(items)
    items = sorted(items, reverse=True)

    # 'uniques' is a list of tuples, where each tuple equal the index of the first
    # occurence of a value, and the value corresponding to this index.
    # This helps to reduce the number of time the recursive method is run
    uniques = find_uniques(items)

    sys.setrecursionlimit(6000)
    original_stdout = sys.stdout

    # Following two blocks print the result either in a file or in the stdout, depending
    # on personnal choice
    # If the debug is enabled, it increase a lot the execution time. It is faster to
    # print in this case in a file rather than in the stdout

    # Block: file out.txt
    with open("out.txt", "w") as f:
        sys.stdout = f
        res, remaining = runner(items, items_len, uniques, debug)
        print(f"For {sum(items) / limit} potential compos,")
        print(f"\n{len(res)} compos can be really obtained\nBatches are:\n{res}")
        sys.stdout = original_stdout

    # Block: stdout
    # print(f"For {sum(items) / limit} potential compos,\n")
    # print(
    #     f"{len(res)} compos can be really obtained\nBatches are:\n{res}\n"
    #     f"Remaining items are:\n{compute_values_from_indexes(items, remaining)}"
    # )
