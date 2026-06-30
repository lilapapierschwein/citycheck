from fastapi.templating import Jinja2Templates

from citycheck import get_config

app_config = get_config()

templates = Jinja2Templates(directory=app_config.paths.directories.templates)
