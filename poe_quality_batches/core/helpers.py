def find_next_index(indexes: list, index: int) -> int:
    # Return the next available index
    while index in indexes:
        index += 1
    return index


def is_there_remaining(items_len: int, indexes: list, index: int) -> bool:
    # Return next available index
    i = find_next_index(indexes, index)
    if i < items_len:
        return True
    return False


def find_remaining(items_len: int, items: list, indexes: list) -> list:
    # Debug method
    rem = [x for x in range(items_len)]
    for i in range(items_len):
        if i in indexes:
            rem.remove(i)
    # rem_items = [items[x] for x in range(items_len) if x in rem]
    return rem


def find_adding_errors(items: list, batches: list):
    # Debug method
    b = list()
    for _b in batches:
        b.extend(_b)
    _items = items.copy()
    for i in b:
        try:
            _items.remove(i)
        except ValueError:
            print(f"Too much item ({i}) in batches")
