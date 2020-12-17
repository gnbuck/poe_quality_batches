from settings.settings import GEM_DESCRIPTION, FLASK_DESCRIPTION


def filter_quality_from_stash(stash_content: dict) -> dict:
    stash_item_qualities = {}
    stash_item_qualities["flasks"] = []
    stash_item_qualities["gems"] = []
    for item in stash_content:
        if is_gem(item) and is_quality_item(item):
            item_quality = int(item["properties"][-1]["values"][0][0][1:-1])
            stash_item_qualities["gems"].append(item_quality)
        elif is_flask(item) and is_quality_item(item):
            item_quality = int(item["properties"][0]["values"][0][0][1:-1])
            stash_item_qualities["flasks"].append(item_quality)
    return stash_item_qualities


def is_gem(item: dict) -> bool:
    try:
        if GEM_DESCRIPTION in item.get("descrText", None):
            return True
    except TypeError:
        # Workaround because for some items, the get function can't parse the dict
        pass
    return False


def is_flask(item: dict) -> bool:
    try:
        if FLASK_DESCRIPTION in item.get("descrText", None):
            return True
    except TypeError:
        pass
    return False


def is_quality_item(item: dict) -> bool:
    try:
        for prop in item["properties"]:
            if prop["name"] == "Quality":
                return True
    except KeyError:
        pass
    return False
