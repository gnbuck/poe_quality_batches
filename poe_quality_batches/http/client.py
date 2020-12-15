import json
import requests

from .helpers import filter_quality_from_stash
from settings.settings import SPECIAL_TABS


def client(
    url: str,
    account: str,
    realm: str,
    league: str,
    character: str,
    poesessid: str,
    object_type: str,
    stash_name: str,
) -> list:
    """Gather inventory from web site and return a comprehensible list by the script."""

    stash_list = get_stash_list(
        url,
        account,
        realm,
        league,
        character,
        poesessid,
        stash_name,
    )
    if stash_name is not None:
        stash_list = [stash for stash in stash_list if stash_name in stash["n"]]

    formatted_stash_list = [
        {"name": stash["n"], "id": stash["i"], "type": stash["type"]}
        for stash in stash_list
        if stash["type"] not in SPECIAL_TABS
    ]

    stashes_with_quality_items = [
        {
            "id": stash_metadata["id"],
            "name": stash_metadata["name"],
            "type": stash_metadata["type"],
            "results": {},
            "items": filter_quality_from_stash(
                get_stash_content(
                    url,
                    account,
                    realm,
                    league,
                    character,
                    poesessid,
                    stash_metadata,
                ),
            ),
        }
        for stash_metadata in formatted_stash_list
    ]

    stashes = [
        stash
        for stash in stashes_with_quality_items
        if len(stash["items"]["gems"]) > 0 or len(stash["items"]["flasks"]) > 0
    ]
    print(f"\nfiltered_stashes = {stashes}\n")

    return stashes


def get_stash_list(
    url: str,
    account: str,
    realm: str,
    league: str,
    character: str,
    poesessid: str,
    stash_name: str,
) -> list:
    """Gather the complete list of one character's stashes."""
    cookies = {
        "POESESSID": poesessid,
    }
    params = {
        "accountName": account,
        "realm": realm,
        "league": league,
        "tabs": 1,
        "tabIndex": 0,
        "character": character,
    }
    response = requests.get(url, cookies=cookies, params=params)
    response_data = json.loads(response.text)
    stash_list = response_data.get("tabs", [])

    return stash_list


def get_stash_content(
    url: str,
    account: str,
    realm: str,
    league: str,
    character: str,
    poesessid: str,
    stash_metadata: dict,
) -> list:
    """Gather the content of one stash."""
    cookies = {
        "POESESSID": poesessid,
    }
    params = {
        "accountName": account,
        "realm": realm,
        "league": league,
        "tabs": 0,
        "tabIndex": stash_metadata["id"],
        "character": character,
    }
    response = requests.get(url, cookies=cookies, params=params)
    response_data = json.loads(response.text)
    stash_content = response_data.get("items", [])

    return stash_content
