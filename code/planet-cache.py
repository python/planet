#!/usr/bin/env python3
"""Planet cache tool."""

__authors__ = [
    "Scott James Remnant <scott@netsplit.com>",
    "Jeff Waugh <jdub@perkypants.org>",
]
__license__ = "Python"


import argparse
import configparser
import os
import shelve
import sys
import time

import planet


def usage():
    print("Usage: planet-cache [options] CACHEFILE [ITEMID]...")
    print()
    print("Examine and modify information in the Planet cache.")
    print()
    print("Channel Commands:")
    print(" -C, --channel     Display known information on the channel")
    print(" -L, --list        List items in the channel")
    print(" -K, --keys        List all keys found in channel items")
    print()
    print("Item Commands (need ITEMID):")
    print(" -I, --item        Display known information about the item(s)")
    print(" -H, --hide        Mark the item(s) as hidden")
    print(" -U, --unhide      Mark the item(s) as not hidden")
    print()
    print("Other Options:")
    print(" -h, --help        Display this help message and exit")
    sys.exit(0)


def usage_error(msg, *args):
    print(msg, " ".join(args), file=sys.stderr)
    print("Perhaps you need --help ?", file=sys.stderr)
    sys.exit(1)


def print_keys(item, title):
    keys = item.keys()
    key_len = max([len(k) for k in sorted(keys)])

    print(title + ":")
    for key in sorted(keys):
        if item.key_type(key) == item.DATE:
            value = time.strftime(planet.TIMEFMT_ISO, item[key])
        else:
            value = str(item[key])
        print("    %-*s  %s" % (key_len, key, fit_str(value, 74 - key_len)))


def fit_str(string, length):
    if len(string) <= length:
        return string
    else:
        return string[: length - 4] + " ..."


if __name__ == "__main__":
    ids = []

    parser = argparse.ArgumentParser(
        description="Examine and modify information in the Planet cache."
    )
    parser.add_argument(
        "-C",
        "--channel",
        action="store_const",
        const="channel",
        dest="command",
        help="Display known information on the channel",
    )
    parser.add_argument(
        "-L",
        "--list",
        action="store_const",
        const="list",
        dest="command",
        help="List items in the channel",
    )
    parser.add_argument(
        "-K",
        "--keys",
        action="store_const",
        const="keys",
        dest="command",
        help="List all keys found in channel items",
    )
    parser.add_argument(
        "-I",
        "--item",
        action="store_const",
        const="item",
        dest="command",
        help="Display known information about the item(s)",
    )
    parser.add_argument(
        "-H",
        "--hide",
        action="store_const",
        const="hide",
        dest="command",
        help="Mark the item(s) as hidden",
    )
    parser.add_argument(
        "-U",
        "--unhide",
        action="store_const",
        const="unhide",
        dest="command",
        help="Mark the item(s) as not hidden",
    )
    parser.add_argument("cache_file", help="Cache file to operate on")
    parser.add_argument(
        "item_ids",
        nargs="*",
        help="Item IDs to operate on when using item-related commands",
    )

    args = parser.parse_args()

    # Check if more than one command option was supplied
    if "command" not in args or args.command is None:
        usage_error("One command option must be supplied.")
    elif (
        len(
            {
                key
                for key, value in vars(args).items()
                if key == "command" and value is not None
            }
        )
        > 1
    ):
        usage_error("Only one command option may be supplied")

    # Handle missing cache_file
    if not args.cache_file:
        usage_error("Missing expected cache filename")

    # Handle commands that require item IDs
    if args.command in ["item", "hide", "unhide"] and not args.item_ids:
        usage_error("Missing expected entry ids")

    # Open the cache file directly to get the URL it represents
    try:
        with shelve.open(args.cache_file, "r") as db:
            url = db["url"]
    except KeyError:
        print(f"{args.cache_file}: Probably not a cache file", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{args.cache_file}: {e!s}", file=sys.stderr)
        sys.exit(1)

    # Now do it the right way :-)
    my_planet = planet.Planet(configparser.ConfigParser())
    my_planet.cache_directory = os.path.dirname(args.cache_file)
    channel = planet.Channel(my_planet, url)

    for item_id in args.item_ids:
        if not channel.has_item(item_id):
            print(item_id + ": Not in channel", file=sys.stderr)
            sys.exit(1)

    # Do the user's bidding
    if args.command == "channel":
        print_keys(channel, "Channel Keys")

    elif args.command == "item":
        for item_id in args.item_ids:
            item = channel.get_item(item_id)
            print_keys(item, "Item Keys for %s" % item_id)

    elif args.command == "list":
        print("Items in Channel:")
        for item in channel.items(hidden=True, sorted=True):
            print("    " + item.id)
            print("         " + time.strftime(planet.TIMEFMT_ISO, item.date))
            if hasattr(item, "title"):
                print("         " + fit_str(item.title, 70))
            if hasattr(item, "hidden"):
                print("         (hidden)")

    elif args.command == "keys":
        keys = {}
        for item in channel.items():
            for key in item:
                keys[key] = 1

        keys = sorted(keys.keys())

        print("Keys used in Channel:")
        for key in keys:
            print("    " + key)
        print()

        print("Use --item to output values of particular items.")

    elif args.command == "hide":
        for item_id in args.item_ids:
            item = channel.get_item(item_id)
            if hasattr(item, "hidden"):
                print(item_id + ": Already hidden.")
            else:
                item.hidden = "yes"

        channel.cache_write()
        print("Done.")

    elif args.command == "unhide":
        for item_id in args.item_ids:
            item = channel.get_item(item_id)
            if hasattr(item, "hidden"):
                del item.hidden
            else:
                print(item_id + ": Not hidden.")

        channel.cache_write()
        print("Done.")
