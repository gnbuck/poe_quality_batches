import json
import requests

from .helpers import filter_quality_from_stash
from settings.settings import SPECIAL_TABS


class Client():
    """Gather inventory from web site and return a comprehensible list by the script."""

    def __init__(
        self,
        url: str,
        account: str,
        realm: str,
        league: str,
        character: str,
        poesessid: str,
        object_type: str,
        stash_name: str,
    ):
        self.url = url
        self.cookies = {
            "POESESSID": poesessid,
        }
        self.params = {
            "accountName": account,
            "realm": realm,
            "league": league,
            "character": character,
        }
        self.object_type = object_type
        self.stash_name = stash_name

    def get_content(self):
        stash_list = self.get_stash_list()

        if self.stash_name is not None:
            stash_list = [
                stash for stash in stash_list if self.stash_name in stash["n"]
            ]

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
                    self.get_stash_content(
                        stash_metadata,
                    ),
                ),
            }
            for stash_metadata in formatted_stash_list
        ]

        self.stashes = [
            stash
            for stash in stashes_with_quality_items
            if len(stash["items"]["gems"]) > 0 or len(stash["items"]["flasks"]) > 0
        ]
        print(f"\nfiltered_stashes = {self.stashes}\n")

        return self.stashes

    def get_stash_list(self) -> list:
        """Gather the complete list of one character's stashes."""
        cookies = self.cookies
        params = self.params
        params["tabs"] = 1
        params["tabIndex"] = 0
        print(f"self.url = {self.url}")
        print(f"self.cookies = {self.cookies}")
        print(f"self.params = {self.params}")
        response = requests.get(self.url, cookies=cookies, params=params)
        response_data = json.loads(response.text)
        stash_list = response_data.get("tabs", [])

        return stash_list

    def get_stash_content(self, stash_metadata: dict,) -> list:
        """Gather the content of one stash."""
        cookies = self.cookies
        params = self.params
        params["tabs"] = 0
        params["tabIndex"] = stash_metadata["id"]
        response = requests.get(self.url, cookies=cookies, params=params)
        response_data = json.loads(response.text)
        stash_content = response_data.get("items", [])

        return stash_content
