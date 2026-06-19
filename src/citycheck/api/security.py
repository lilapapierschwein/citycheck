from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from citycheck.core.utils import get_env_var
from citycheck.settings import DOTENV_FILE

# from citycheck.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

PWD_HASH_SECRET_KEY = get_env_var("PWD_HASH_SECRET_KEY", DOTENV_FILE)
PWD_HASH_ALGORITHM = get_env_var("PWD_HASH_ALGORITHM", DOTENV_FILE)
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
