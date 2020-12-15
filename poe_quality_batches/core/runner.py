from .helpers import (
    find_next_index,
    find_remaining,
    find_adding_errors,
    is_there_remaining,
)


def runner(items: list, items_len: int, uniques: list, limit: int, debug: bool):
    best_batches = list()
    best_batches_remaining = list()
    for start in uniques:
        index = -1  # Cursor
        indexes = [start[0]]  # List on every items indexes present in batches
        batch = [start[1]]  # List of current batch based on the items
        batch_indexes = [start[0]]  # List of current batch based on the indexes
        batches, remaining = find_batches(
            items, items_len, limit, indexes, batch, batch_indexes, list(), index, debug
        )
        if len(batches) > len(best_batches):
            best_batches = batches.copy()
            best_batches_remaining = remaining.copy()
    return best_batches, best_batches_remaining


def find_batches(
    items: list,
    items_len: int,
    limit: int,
    indexes: list,
    batch: list,
    batch_indexes: list,
    batches: list,
    index: int,
    debug: bool,
) -> list():

    index += 1
    index = find_next_index(indexes, index)
    if index >= items_len:
        depth = 0
        for i in sorted(batch_indexes, reverse=True):
            # Checking if there is any available index not already taken after each
            # item of the current batch
            if is_there_remaining(items_len, indexes + [index], i) is not True:
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

        if (
            len(batch_indexes) == 0
            or is_there_remaining(items_len, indexes, batch_indexes[0]) is not True
        ):
            remaining = find_remaining(items_len, items, indexes)
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

    if debug is True:
        find_remaining(items_len, items, indexes)
        print(f"items = {items}")
        # DEBUG: check each item can be in batches
        find_adding_errors(items, batches)
        print(
            f"index = {index}\nbatch   = {batch}\nindexes = {indexes}\tbatch_indexes ="
            f"{batch_indexes}\nbatches = {batches}\n"
        )

    return find_batches(
        items,
        items_len,
        limit,
        indexes,
        batch,
        batch_indexes,
        batches,
        index,
        debug,
    )
