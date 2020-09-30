import json
import sys
import time

from samples import SAMPLES
from helpers import (
    find_uniques,
    find_next_index,
    find_remaining,
    compute_values_from_indexes,
    find_adding_errors,
    is_there_remaining,
)
from settings import LIMIT as limit

"""
Description
-----------

This script aims to compute the highest number of batch of 40 that can be obtained by
combining the values (integers) stored in a list.

Todo
----

* Make the script more modular
* Check every available combination

"""

sample = SAMPLES["items_quality_shorten"]
sample0 = SAMPLES["items_quality"]

items = sample0
items_len = len(items)
items = sorted(items, reverse=True)
# 'uniques' is a list of tuples, where each tuple equal the index of the first
# occurence of a value, and the value corresponding to this index.
# This helps to reduce the number of time the recursive method is run
uniques = find_uniques(items)

def run():
    best_batches = list()
    best_batches_remaining = list()
    for start in uniques:
        index = -1                  # Cursor
        indexes = [start[0]]        # List on every items indexes present in batches
        batch = [start[1]]          # List of current batch based on the items
        batch_indexes = [start[0]]  # List of current batch based on the indexes
        batches, remaining = pied(indexes, batch, batch_indexes, list(), index)
        if len(batches) > len(best_batches):
            best_batches = batches.copy()
            best_batches_remaining = remaining.copy()
    return best_batches, best_batches_remaining


def pied(
    indexes:list,
    batch:list,
    batch_indexes:list,
    batches:list,
    index:int
    ) -> list():

    index += 1
    index = find_next_index(indexes, index)
    if index >= items_len:
        depth = 0
        for i in sorted(batch_indexes, reverse=True):
            # Checking if there is any available index not already taken after each
            # item of the current batch
            if is_there_remaining(items_len, indexes+[index], i) is not True:
                # If it is the case, increment the marker
                depth += 1
        if depth:
            # Backtrack in case the lase item of the batch cannot be imcremented.
            # For instance, if the two lasts of a batch of 5 items, are the two last
            # available items, these two must be removed from the current batch.
            # Finally, the script continue to search from the batch of 3 items, with
            # the last incremented
            index = find_next_index(indexes, batch_indexes[len(batch_indexes) - depth])
            for _ in range(depth):
                indexes.pop()
                batch.pop()
                batch_indexes.pop()
            index = find_next_index(indexes, index)
        else:
            # Else, if the last item of the batch can be incremented, do
            batch_indexes[-1] = find_next_index(indexes, batch_indexes[-1])
            batch[-1] = items[batch_indexes[-1]]
            indexes[-1] = batch_indexes[-1]
            index = find_next_index(indexes, batch_indexes[-1])

        try:    
            if is_there_remaining(items_len, indexes, batch_indexes[0]) is not True:
                # Win condition
                # Occurs when there is no more available items after the first item in
                # the batch
                raise IndexError
        except IndexError:
            remaining = find_remaining(items, indexes)
            return batches, remaining

    if index < items_len:
        if sum(batch) + items[index] < limit:
            # Add to the current batch
            indexes.append(index)
            batch.append(items[index])
            batch_indexes.append(index)
        elif sum(batch) + items[index] == limit:
            # This implementation does not allow to test each order
            # Save the current batch
            indexes.append(index)
            batch.append(items[index])
            batches.append(batch)
            # Start a new batch
            batch_indexes = [find_next_index(indexes, min(batch_indexes))]
            indexes.append(batch_indexes[-1])
            batch = [items[batch_indexes[-1]]]
            index = batch_indexes[-1]
        elif sum(batch) + items[index] > limit:
            pass
    
    # # Uncomment the following to enable debug
    # # DEBUG: remaining items and indexes
    # find_remaining(items, indexes)
    # print(f"items = {items}")
    # # DEBUG: check each item can be in batches
    # find_adding_errors(items, batches)
    # print(
    #     f"index = {index}\nbatch   = {batch}\nindexes = {indexes}\tbatch_indexes ="
    #     + f"{batch_indexes}\nbatches = {batches}"
    # )

    return pied(indexes, batch, batch_indexes, batches, index)

sys.setrecursionlimit(6000)
original_stdout = sys.stdout
with open("out.txt", "w") as f:
    # Since the debug increase a lot the execution time, it is faster to print in a
    # file rather than in the stdout
    sys.stdout = f
    res, remaining = run()
    print(f"For {sum(items) / limit} potential compos,")
    print(f"\n{len(res)} compos can be really obtained\nBatches are:\n{res}")
    sys.stdout = original_stdout

print(
    f"\n{len(res)} compos can be really obtained\nBatches are:\n{res}\n"
    + f"Remaining items are:\n{compute_values_from_indexes(items, remaining)}"
)
