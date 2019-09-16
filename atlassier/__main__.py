import argparse
import configparser
import logging
import os

from atlassier.atlassian import Atlassian
from atlassier.inventory import Inventory


def add(args, atlassian):
    print("Adding")


def fetch(args, atlassian):
    atlassian.fetch()


def parse_args_add(subparsers):
    parser = subparsers.add_parser("add", help="New resources")
    parser.set_defaults(handler=add)

    parser.add_argument("resource", choices=["repository"], help="Type of resource")


def parse_args_fetch(subparsers):
    parser = subparsers.add_parser("fetch", help="Resources information")
    parser.set_defaults(handler=fetch)


def parse_args():
    parser = argparse.ArgumentParser(description="GitOps for Atlassian products")

    parser.add_argument(
        "--inventory", default=".", help="Directories to be used as inventory."
    )
    parser.add_argument(
        "--dry-run",
        default=False,
        action="store_true",
        help="Do not modify the environment",
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )
    subparsers = parser.add_subparsers(help="Actions")
    parse_args_add(subparsers)
    parse_args_fetch(subparsers)

    return parser.parse_args()


def configure_logging(verbosity):
    msg_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    VERBOSITIES = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    level = VERBOSITIES[min(int(verbosity), len(VERBOSITIES) - 1)]
    formatter = logging.Formatter(msg_format)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(level)


def main():
    args = parse_args()
    configure_logging(args.verbose)
    config = config = configparser.ConfigParser()
    config.read(["atlassier.cfg", os.path.expanduser("~/.atlassier/atlassier.cfg")])

    inventory = Inventory(args.inventory)
    inventory.load()

    atlassian = Atlassian(
        inventory=inventory,
        dry_run=args.dry_run,
        credentials=dict(
            username=config.get("credentials", "username"),
            password=config.get("credentials", "password"),
        ),
    )
    args.handler(args, atlassian)


if __name__ == "__main__":
    main()
