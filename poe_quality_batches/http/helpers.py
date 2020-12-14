def format_stash_list(stash_list: list) -> list:
    _stash_list = [
        {"name": stash["n"], "id": stash["i"], "type": stash["type"]}
        for stash in stash_list
    ]
    return _stash_list


def format_stash_content(stash_content: dict) -> dict:
    stash_item_qualities = []
    for item in stash_content:
        item_quality = int(item["properties"][0]["values"][0][0][1:-1])
        stash_item_qualities.append(item_quality)
    return stash_item_qualities


def check_object_type(obj, obj_type):
    raise NotImplementedError()


def find_quality_objects():
    raise NotImplementedError()


def is_flask(item: dict) -> bool:
    flask_description = (
        "Right click to drink. "
        "Can only hold charges while in belt. "
        "Refills as you kill monsters."
    )
    if flask_description in item["descrText"]:
        return True
    return False


def is_gem(item: dict) -> bool:
    raise NotImplementedError()
