from fastapi.templating import Jinja2Templates

from citycheck.settings import TEMPLATES_DIR

templates = Jinja2Templates(directory=TEMPLATES_DIR)
