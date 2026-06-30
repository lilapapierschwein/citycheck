from colorama import Fore, Style

from citycheck import get_config
from citycheck.api.crud import create_user
from citycheck.api.crud.user import add_user_activity, set_password
from citycheck.api.models.user import UserCreate
from citycheck.api.security import hash_password, password_is_valid
from citycheck.core.utils.enums import UserAction
from citycheck.db.db import init_db

# from .cli import parse_args
from .data import get_initial_data
from .inserts import insert_initial_data
from .utils import get_term_width, print_headline

app_config = get_config()
filepaths = app_config.paths.files


async def run_setup(
    rebuild_db: bool = False,
    update_init_data: bool = False,
    insert_testuser: bool = False,
    verbose: bool = True,
):
    db_file, init_data_file = filepaths.db, filepaths.init_data
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
    if not filepaths.init_data.exists() or update_init_data:
        if verbose:
            print("creating/updating init data...", end="\r")
        get_initial_data(init_data_file)

    print_headline("initializing database...", text_width)

    db = init_db(db_file)
    if verbose:
        print(f"database initialized...{Fore.GREEN}DONE{Style.RESET_ALL}")
        if rebuild_db:
            print(f"database (re-)created at {db_file}...{Fore.GREEN}DONE{Style.RESET_ALL}")

    with db.get_session() as Session:
        insert_initial_data(
            file=init_data_file, session=Session, text_width=text_width, verbose=verbose
        )

        if insert_testuser:
            if verbose:
                print("inserting testuser...", end="\r")
            testuser_data = {"username": "testuser", "email": "testuser@example.com"}
            testuser = await create_user(UserCreate.model_validate(testuser_data), Session)

            passwd = "testUs3R@cc01!!"
            if not password_is_valid(passwd):
                raise ValueError("Invalid password")
            _ = await set_password(testuser, hash_password(passwd), Session)
            _ = await add_user_activity(testuser, UserAction.SIGNUP, Session)
            if verbose:
                print(f"inserting testuser...{Fore.GREEN}DONE{Style.RESET_ALL}")
                print(
                    f"INSERT: [user#{testuser.id}] {testuser} ({testuser.email}) | password: '{passwd}'"
                )

    if verbose:
        print_headline(
            "initial data inserted successfully. setup finished.",
            text_width,
            color="green",
        )


def main() -> None:
    return
    # args = parse_args()
    # run_setup(
    #     rebuild_db=args.rebuild_db,
    #     update_init_data=args.update_data,
    #     insert_testuser=args.testuser,
    #     verbose=True,
    # )


if __name__ == "__main__":
    main()
