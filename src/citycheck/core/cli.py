# pyright: reportPrivateUsage=false

import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace, _SubParsersAction
from collections.abc import Callable
from time import sleep
from typing import Literal

from citycheck.core.setup.setup import run_setup
from citycheck.core.utils import APIDefaults
from citycheck.core.utils.utils import api_is_running, init_api_shutdown
from citycheck.settings import API_DEFAULTS

from citycheck.api.main import main as api_main

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
    _ = api_parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=defaults["port"],
        help="specify port to use.",
    )
    _ = api_parser.add_argument(
        "-v",
        "--use-version",
        type=str,
        choices=[1],
        default=defaults["version"],
        help="specify api-version.",
    )

    api_cmds = api_parser.add_subparsers(title="commands", dest="api_cmd", required=False)
    _ = api_cmds.add_parser("start")
    _ = api_cmds.add_parser("stop")

    return api_parser


parser_creators: list[Callable[[SubParserType], ArgumentParser]] = [
    create_setup_parser,
    create_api_parser,
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


def start_api(port: int | None = None) -> None:
    is_running, msg = api_is_running()
    if is_running:
        print(f"API is already running (status: {repr(msg)})")
        return

    print(f"Starting API on port {port or 8000}...")
    api_main(port)


def shutdown_api() -> None:
    is_running, msg = api_is_running()
    if not is_running:
        print("api is not running")
        return
    print("Shutting down server...")

    is_shutting_down, msg = init_api_shutdown()
    if is_shutting_down:
        print(msg)
    else:
        print("error:", msg)
        return

    while True:
        sleep(1)
        is_running, msg = api_is_running()
        if not is_running:
            print("Server shutdown successfully.")
            break
        print("error:", msg)
    return None


def run_cli() -> None:
    parsed_args = parse_sys_args()
    cmd: Literal["setup", "api"] | None = parsed_args.cmd or None
    if not cmd:
        return None

    match cmd:
        case "setup":
            run_setup(
                rebuild_db=parsed_args.rebuild_db or False,
                update_init_data=parsed_args.update_data or False,
                insert_testuser=parsed_args.testuser or False,
                verbose=not (parsed_args.quiet or False),
            )
        case "api":
            api_cmd: Literal["start", "stop"] | None = parsed_args.api_cmd
            if not api_cmd:
                return
            match api_cmd:
                case "start":
                    start_api(parsed_args.port or 8000)
                case "stop":
                    shutdown_api()


def main() -> None:
    run_cli()


if __name__ == "__main__":
    main()


# def create_parser(prog: str = PROG, version: str = VERSION) -> ArgumentParser:
#     parser = ArgumentParser(
#         prog=prog, formatter_class=ArgumentDefaultsHelpFormatter, description="set up citycheck."
#     )
#
#     _ = parser.add_argument("-V", "--version", action="version", version=f"{prog} {version}")
#
#     sub_parsers = parser.add_subparsers(
#
#     )
#
#     _ = parser.add_argument(
#         "-d",
#         "--rebuild-db",
#         action="store_true",
#         help="remove existing db file and re-create database from scratch.",
#     )
#     _ = parser.add_argument(
#         "-u",
#         "--update-data",
#         action="store_true",
#         help="update db init data via restcountries api. requires valid api-key.",
#     )
#     _ = parser.add_argument(
#         "-t",
#         "--testuser",
#         action="store_true",
#         help="insert a test user-account named 'testuser'.",
#     )
#     _ = parser.add_argument(
#         "-v",
#         "--no-verbose",
#         action="store_false",
#         help="do not show verbose output.",
#     )
#
#     return parser
