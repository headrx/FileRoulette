#!/usr/bin/env python3

"""FileRoulette: Find random data on various hosting services.

This script is used to execute the FileRoulette module from the command-line
directly.
"""

import argparse
import sys

from fileroulette import DESCRIPTION, MODULE_DICT, run_module

if __name__ == "__main__":
    # Parse the command-line arguments.
    argparser = argparse.ArgumentParser(description=DESCRIPTION)
    argparser.add_argument(
        "-a",
        dest="agent",
        action="store_true",
        help="enable random user-agent",
    )
    argparser.add_argument(
        "-p",
        dest="proxy",
        action="store_true",
        help="enable proxies (requires a proxies.txt file)",
    )
    argparser.add_argument(
        "-m",
        dest="module",
        default="list",
        help="choose data source module (omit to list available modules)",
    )
    args = argparser.parse_args()

    # See if they defined a source module.
    if args.module == "list":
        # No module was defined. List the available modules, then exit.
        print(f"{DESCRIPTION}\n\nAvailable modules:\n------------------")
        # Retrieve the list of module names from the MODULE_DICT.
        keys = list(MODULE_DICT.keys())
        # Sort the list alphabetically.
        keys.sort()
        # Get the width of the longest name in the list.
        width = len(max(keys, key=len))
        # Print out the module list, padding each line so that the descriptions
        # of the modules are aligned.
        for key in keys:
            module = MODULE_DICT[key]
            print(
                "- {}{}  {}".format(
                    key, " " * (width - len(key)), module.description
                )
            )
        print("\nFor usage information, type {} --help".format(sys.argv[0]))
        # Exit the program.
        sys.exit(0)

    # Ensure the module is valid.
    if args.module not in MODULE_DICT.keys():
        # The module doesn't exist. Inform the user, and tell them how to get
        # a list of available modules.
        print(f"Error: Module '{args.module}' doesn't exist.")
        print(f"For a list of modules, simply run {sys.argv[0]}.")
        sys.exit(0)

    # Run the specified module.
    run_module(args.module, agent=args.agent, proxy=args.proxy)
