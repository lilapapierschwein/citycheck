from fastapi.templating import Jinja2Templates

from citycheck.settings import APP_CONFIG

templates = Jinja2Templates(directory=APP_CONFIG.files.dirs.templates)
