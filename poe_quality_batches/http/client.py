import json
import requests

from .helpers import format_stash_list, format_stash_content


def client(
    url: str,
    account: str,
    realm: str,
    league: str,
    character: str,
    tab_index: str,
    poesessid: str,
    object_type: str,
    force_object_type: bool,
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

    stash_contents = [
        get_stash_content(
            url,
            account,
            realm,
            league,
            character,
            poesessid,
            object_type,
            stash_metadata,
        )
        for stash_metadata in stash_list
    ]

    formatted_stash_contents = [
        format_stash_content(stash_content) for stash_content in stash_contents
    ]

    return formatted_stash_contents


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

    if stash_name is not None:
        stash_list = [stash for stash in stash_list if stash_name in stash["n"]]

    stash_list = format_stash_list(stash_list)

    return stash_list


def get_stash_content(
    url: str,
    account: str,
    realm: str,
    league: str,
    character: str,
    poesessid: str,
    object_type: str,
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
