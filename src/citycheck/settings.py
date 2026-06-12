from pathlib import Path

APP_NAME = "citycheck"
ROOT = Path(__file__).parent.parent.parent
DATA_DIR = ROOT / "data"
DB_FILE = DATA_DIR / f"{APP_NAME}.db"
