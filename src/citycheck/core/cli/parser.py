import sys
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    Namespace,
    _SubParsersAction,  # pyright: ignore[reportPrivateUsage]
)
from collections.abc import Callable
from pathlib import Path

from citycheck.core.utils import APIDefaults
from citycheck.settings import API_DEFAULTS, SRC_DIR

PROG = "citycheck"
VERSION = "0.1.0"


type SubParserType = _SubParsersAction[ArgumentParser]


def create_setup_parser(
    parser: SubParserType, name: str = "setup", prog: str = PROG, version: str = VERSION
) -> ArgumentParser:
    setup_parser = parser.add_parser(name)

    _ = setup_parser.add_argument(
        "-V", "--version", action="version", version=f"{prog} {name} {version}"
    )
    _ = setup_parser.add_argument(
        "-d",
        "--rebuild-db",
        action="store_true",
        help="remove existing db file and re-create database from scratch.",
    )
    _ = setup_parser.add_argument(
        "-u",
        "--update-data",
        action="store_true",
        help="update db init data via restcountries api. requires valid api-key.",
    )
    _ = setup_parser.add_argument(
        "-t",
        "--testuser",
        action="store_true",
        help="insert a test user-account named 'testuser'.",
    )
    _ = setup_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="do not show verbose output.",
    )
    return setup_parser


def create_api_parser(
    parser: SubParserType,
    name: str = "api",
    prog: str = PROG,
    version: str = VERSION,
    defaults: APIDefaults = API_DEFAULTS,
):
    api_parser = parser.add_parser(name)

    _ = api_parser.add_argument("-V", "--version", action="version", version=f"{prog} {version}")

    api_cmds = api_parser.add_subparsers(title="commands", dest="api_cmd", required=False)

    api_start_parser = api_cmds.add_parser(
        "start", help="start api server with specified arguments."
    )
    _ = api_start_parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=defaults["port"],
        help=f"specify port to use. (default: {defaults['port']})",
    )
    _ = api_start_parser.add_argument(
        "-v",
        "--use-version",
        type=str,
        choices=[1],
        default=defaults["version"],
        help=f"specify api-version. (default: {defaults['version']})",
    )

    _ = api_cmds.add_parser("stop", help="issue a shutdown signal to the api server.")

    return api_parser


def create_dev_parser(
    parser: SubParserType,
    name: str = "dev",
    prog: str = PROG,
    version: str = VERSION,
):
    dev_parser = parser.add_parser(name)

    _ = dev_parser.add_argument("-V", "--version", action="version", version=f"{prog} {version}")

    dev_cmds = dev_parser.add_subparsers(title="commands", dest="dev_cmd", required=False)
    loc_parser = dev_cmds.add_parser("count-lines")
    _ = loc_parser.add_argument(
        "-m",
        "--mode",
        type=str,
        choices=["plain", "json"],
        default="plain",
        help="set output mode.",
    )
    _ = loc_parser.add_argument("-o", "--output", type=Path, help="redirect output to file")
    _ = loc_parser.add_argument(
        "-t", "--filetypes", nargs="*", help="specify filetypes for count."
    )
    _ = loc_parser.add_argument(
        "-i", "--ignore", nargs="*", help="files to ignore. full name with suffix."
    )
    _ = loc_parser.add_argument(
        "-e", "--include-empty-lines", action="store_true", help="include empty lines."
    )
    _ = loc_parser.add_argument(
        "path", type=Path, default=SRC_DIR, nargs="?", help="target directory. (default: src/)"
    )

    return dev_parser


parser_creators: list[Callable[[SubParserType], ArgumentParser]] = [
    create_setup_parser,
    create_api_parser,
    create_dev_parser,
]


def create_main_parser(
    prog: str = PROG,
    version: str = VERSION,
    subparsers_creators: list[Callable[[SubParserType], ArgumentParser]] = parser_creators,
) -> ArgumentParser:
    parser = ArgumentParser(prog=prog, formatter_class=ArgumentDefaultsHelpFormatter)
    _ = parser.add_argument("-V", "--version", action="version", version=f"{prog} {version}")

    commands_parser = parser.add_subparsers(
        title="commands", help="command to use", dest="cmd", required=False
    )

    for spc in subparsers_creators:
        _ = spc(commands_parser)

    return parser


def parse_sys_args(sys_args: list[str] = sys.argv[1:]) -> Namespace:
    parser = create_main_parser()
    return parser.parse_args(sys_args)
