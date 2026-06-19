from pathlib import Path

from .utils import get_project_root

APP_NAME = "citycheck"  # should have the same name as your project root dir
ROOT_MARKERS = ["pyproject.toml", ".gitignore", ".venv"]
DATA_DIR_NAME = "data"
INIT_DATA_FILE_NAME = "init_data.json"
DOTENV_FILE_NAME = ".env"

# WARN: do not change anything below unless you know what you are doing! #######
ROOT = get_project_root(
    file=Path(__file__),
    root_markers=ROOT_MARKERS,
    project_name=APP_NAME,
    user_home=Path.home(),
)
DATA_DIR = ROOT / DATA_DIR_NAME
INIT_DATA_FILE = DATA_DIR / INIT_DATA_FILE_NAME
DB_FILE = DATA_DIR / f"{APP_NAME}.db"
SRC_DIR = ROOT / "src"
WEB_DIR = SRC_DIR / "web"
STATIC_DIR = WEB_DIR / "static"
TEMPLATES_DIR = WEB_DIR / "templates"
DOTENV_FILE = ROOT / DOTENV_FILE_NAME
