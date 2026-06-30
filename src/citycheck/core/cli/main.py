import sys
from typing import Any, Literal

from citycheck import get_config
from citycheck.core.setup.setup import run_setup
from citycheck.core.utils.dev import count_lines_cli

from .parser import create_main_parser
from .utils import create_db_backup, shutdown_api, start_api

app_config = get_config()

PROG = app_config.app_name
VERSION = app_config.version


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
            dev_cmd: Literal["count-lines", "db-backup"] | None = parsed_args.dev_cmd
            if not dev_cmd:
                return None
            match dev_cmd:
                case "count-lines":
                    count_lines_cli(parsed_args)
                case "db-backup":
                    bak_data: dict[str, Any] = {
                        "db_file": parsed_args.file,
                        "backup_name": parsed_args.name,
                        "backup_dir": parsed_args.dir,
                        "remove_existing": parsed_args.remove_existing,
                    }

                    empty_keys: list[str] = []
                    for k, v in bak_data.items():
                        if v is None:
                            empty_keys.append(k)
                    if empty_keys:
                        for ek in empty_keys:
                            del bak_data[ek]
                    backup = create_db_backup(**bak_data) if bak_data else create_db_backup()
                    if backup is None:
                        print("Backup failed.")
                        return
                    print(f"Backup successful: ./{backup.relative_to(app_config.paths.root)}")
    return None


def main() -> None:
    try:
        run_cli()
    except RuntimeError as err:
        print("error:", err)


if __name__ == "__main__":
    main()
