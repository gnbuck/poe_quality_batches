import argparse
from os import environ

from distutils.util import strtobool

from poe_quality_batches import main

# from poe_quality_batches.quality_batches import main
from poe_quality_batches.helpers import parse_object_type
from settings.settings import LIMIT, OBJECT_TYPES

if __name__ == "__main__":
    # HTTP vars
    account = environ.get("ACCOUNT", None)
    character = environ.get("CHARACTER", None)
    realm = environ.get("REALM", None)
    league = environ.get("LEAGUE", None).capitalize()
    poesessid = environ.get("POESESSID", None)

    # Script vars
    object_type = parse_object_type(OBJECT_TYPES, environ.get("OBJECT_TYPE", None))
    stash_name = environ.get("STASH_NAME", None)

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
        object_type,
        stash_name,
        online,
        LIMIT,
        debug,
    )
