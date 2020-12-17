import argparse

# from os import environ

from distutils.util import strtobool

from poe_quality_batches import main

from config import (
    ACCOUNT,
    CHARACTER,
    REALM,
    LEAGUE,
    POESESSID,
)

try:
    from config import OBJECT_TYPE
except ImportError:
    OBJECT_TYPE = None
try:
    from config import STASH_NAME
except ImportError:
    STASH_NAME = None
from poe_quality_batches.helpers import parse_object_type
from settings.settings import LIMIT, OBJECT_TYPES

if __name__ == "__main__":
    # HTTP vars
    account = ACCOUNT
    character = CHARACTER
    realm = REALM
    league = LEAGUE
    poesessid = POESESSID

    # Script vars
    object_type = parse_object_type(OBJECT_TYPES, OBJECT_TYPE)
    stash_name = STASH_NAME

    parser = argparse.ArgumentParser(allow_abbrev=True)
    parser.add_argument(
        "--online",
        type=str,
        default="true",
        help="If the script must query online the content of an inventory or read the"
        "input from a hardcoded list",
    )
    parser.add_argument(
        "--debug",
        type=str,
        default="false",
        help="Print each iteration of the script in a file",
    )
    args = parser.parse_args()
    online = bool(strtobool(args.online))
    debug = bool(strtobool(args.debug))

    main(
        account,
        realm,
        league,
        character,
        poesessid,
        online,
        LIMIT,
        object_type,
        stash_name,
        debug,
    )
