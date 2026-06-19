import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace

PROG = "citycheck-setup"
VERSION = "0.1.0"


def create_parser(prog: str = PROG, version: str = VERSION) -> ArgumentParser:
    parser = ArgumentParser(
        prog=prog, formatter_class=ArgumentDefaultsHelpFormatter, description="set up citycheck."
    )

    _ = parser.add_argument("-V", "--version", action="version", version=f"{prog} {version}")
    _ = parser.add_argument(
        "-d",
        "--rebuild-db",
        action="store_true",
        help="remove existing db file and re-create database from scratch.",
    )
    _ = parser.add_argument(
        "-u",
        "--update-data",
        action="store_true",
        help="update db init data via restcountries api. requires valid api-key.",
    )
    _ = parser.add_argument(
        "-t",
        "--testuser",
        action="store_true",
        help="insert a test user-account named 'testuser'.",
    )
    _ = parser.add_argument(
        "-v",
        "--no-verbose",
        action="store_false",
        help="do not show verbose output.",
    )

    return parser


def parse_args(args: list[str] = sys.argv[1:]) -> Namespace:
    parser = create_parser()
    return parser.parse_args(args=args)
