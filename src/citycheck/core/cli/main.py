import sys
from typing import Literal

from citycheck.core.setup.setup import run_setup
from citycheck.core.utils.dev import count_lines_cli

from .parser import create_main_parser
from .utils import shutdown_api, start_api

PROG = "citycheck"
VERSION = "0.1.0"


def run_cli() -> None:
    parser = create_main_parser()
    parsed_args = parser.parse_args(sys.argv[1:])

    cmd: Literal["setup", "api", "dev"] | None = parsed_args.cmd or None
    if not cmd:
        parser.print_help()
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
        case "dev":
            dev_cmd: Literal["count-loc"] | None = parsed_args.dev_cmd
            if not dev_cmd:
                return None
            count_lines_cli(parsed_args)
    return None


def main() -> None:
    run_cli()


if __name__ == "__main__":
    main()
