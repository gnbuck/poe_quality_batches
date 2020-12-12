import argparse

from distutils.util import strtobool

from poe_quality_batches.quality_batches import main

if __name__ == "__main__":
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
    main(online, debug)
