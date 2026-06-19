# from citycheck.core.cli.main import run_cli


from citycheck.settings import APP_CONFIG


def main() -> None:
    print(APP_CONFIG)
    # run_cli()
    # backup = create_db_backup()
    # if not backup:
    #     return None
    # print(f"database backup successfully created at ./{backup.relative_to(ROOT)}")

    # cfg = AppConfigNew.model_validate(load_toml_data(Path.cwd() / "cfg.toml"))
    # print(cfg.root)
    # root = get_project_root(Path.cwd(), cfg.files.root_markers, cfg.general.app_name, Path.home())
