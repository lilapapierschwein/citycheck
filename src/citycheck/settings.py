from pathlib import Path

APP_NAME = "citycheck"
ROOT = Path(__file__).parent.parent.parent
DATA_DIR = ROOT / "data"
INIT_DATA_FILE = DATA_DIR / "init_data.json"
DB_FILE = DATA_DIR / f"{APP_NAME}.db"
SRC_DIR = ROOT / "src"
WEB_DIR = SRC_DIR / "web"
STATIC_DIR = WEB_DIR / "static"
TEMPLATES_DIR = WEB_DIR / "templates"
DOTENV_FILE = ROOT / ".env"
