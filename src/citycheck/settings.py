from pathlib import Path

from citycheck.core.utils import get_project_root, load_app_config

# the app name should have the same name as your project root directory
APP_NAME = "citycheck"
ROOT_MARKERS = ["pyproject.toml", ".gitignore", ".venv"]
CONFIG_FILE_NAME = "app_config.toml"

# WARN: do not change the lines below *unless* you know what you are doing!
ROOT = get_project_root(
    file=Path(__file__),
    root_markers=ROOT_MARKERS,
    project_name=APP_NAME,
    user_home=Path.home(),
)

CONFIGS_DIR = ROOT
CONFIG_FILE = CONFIGS_DIR / CONFIG_FILE_NAME
cfg = load_app_config(CONFIG_FILE)

DATA_DIR = ROOT / cfg.data_dir
INIT_DATA_FILE = DATA_DIR / cfg.init_data_file
DB_FILE = DATA_DIR / f"{APP_NAME}.db"
SRC_DIR = ROOT / "src"
WEB_DIR = SRC_DIR / "web"
STATIC_DIR = WEB_DIR / "static"
TEMPLATES_DIR = WEB_DIR / "templates"
DOTENV_FILE = ROOT / cfg.dotenv_file

DEFAULTS = cfg.defaults
API_DEFAULTS = cfg.defaults["api"]
