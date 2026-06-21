from fastapi.templating import Jinja2Templates

from citycheck import app_config

templates = Jinja2Templates(directory=app_config.paths.directories.templates)
