from colorama import Fore, Style

from citycheck.db.db import init_db
from citycheck.db.models import (
    User,
)
from citycheck.settings import DB_FILE, INIT_DATA_FILE

from .data import get_initial_data
from .inserts import insert_initial_data
from .utils import get_term_width, print_headline


def run_setup(
    rebuild_db: bool = False,
    update_init_data: bool = False,
    insert_testuser: bool = False,
    verbose: bool = True,
):
    db_file, init_data_file = DB_FILE, INIT_DATA_FILE
    text_width = 80 if not verbose else get_term_width()

    if verbose:
        print_headline("citycheck setup", text_width)
        print(
            "options:",
            f"  *rebuild_db:        {rebuild_db}",
            f"  *update_init_data:  {update_init_data}",
            f"  *insert_testuser:   {insert_testuser}",
            sep="\n",
        )
        print_headline("starting setup...", text_width)

    if rebuild_db and db_file.exists():
        if verbose:
            print(f"deleting database file: {db_file}...", end="\r")
        db_file.unlink()
        if verbose:
            print(
                f"deleting database file: {db_file}...{Fore.GREEN}DONE{Style.RESET_ALL}",
            )
    if not INIT_DATA_FILE.exists() or update_init_data:
        if verbose:
            print("creating/updating init data...")
        get_initial_data(init_data_file)

    print_headline("initializing database...", text_width)

    db = init_db(db_file)
    if verbose:
        if rebuild_db:
            print(
                f"database (re-)created at {db_file}...{Fore.GREEN}DONE{Style.RESET_ALL}"
            )
        print(f"database initialized...{Fore.GREEN}DONE{Style.RESET_ALL}")

    with db.get_session() as Session:
        insert_initial_data(
            file=init_data_file, session=Session, text_width=text_width, verbose=verbose
        )

        if insert_testuser:
            if verbose:
                print("inserting testuser...", end="\r")
            testuser = User(username="testuser", email="testuser@example.com")
            Session.add(testuser)
            Session.commit()
            if verbose:
                print(f"inserting testuser...{Fore.GREEN}DONE{Style.RESET_ALL}")
                print(f"INSERT: [user#{testuser.id}] {testuser} ({testuser.email})")

    if verbose:
        print_headline(
            "initial data inserted successfully. setup finished.",
            text_width,
            color="green",
        )


def main() -> None:
    run_setup(
        rebuild_db=True, update_init_data=True, insert_testuser=True, verbose=True
    )


if __name__ == "__main__":
    main()
