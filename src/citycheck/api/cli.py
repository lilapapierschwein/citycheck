import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace

from citycheck.core.utils import APIDefaults
from citycheck.settings import API_DEFAULTS

PROG = "citycheck-api"
VERSION = "0.1.0"


def create_parser(
    prog: str = PROG, version: str = VERSION, defaults: APIDefaults = API_DEFAULTS
) -> ArgumentParser:
    parser = ArgumentParser(
        prog=prog,
        formatter_class=ArgumentDefaultsHelpFormatter,
        description="run the citycheck api.",
    )

    _ = parser.add_argument("-V", "--version", action="version", version=f"{prog} {version}")
    _ = parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=defaults["port"],
        help="specify port to use.",
    )
    _ = parser.add_argument(
        "-v",
        "--use-version",
        type=str,
        choices=[1],
        default=defaults["version"],
        help="specify api-version.",
    )

    return parser


def parse_args(args: list[str] = sys.argv[1:]) -> Namespace:
    parser = create_parser()
    return parser.parse_args(args=args)
