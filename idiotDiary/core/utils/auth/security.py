import base64
import logging
from datetime import datetime

import jwt
from passlib.context import CryptContext

from idiotDiary.core.config.models.auth import SecurityConfig
from idiotDiary.core.utils.dates import tz_utc
from .token import Token

logger = logging.getLogger(__name__)


class SecurityProps:
    def __init__(self, config: SecurityConfig) -> None:
        super().__init__()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = config.secret_key
        self.algorythm = config.algorythm
        self.access_token_expire = config.token_expire
        self.encoding = config.encoding

    def verify_password(
            self, plain_password: str, hashed_password: str
    ) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_token(self, data: dict) -> Token:
        to_encode = data.copy()
        expire = datetime.now(tz=tz_utc) + self.access_token_expire
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorythm
        )
        return Token(value=encoded_jwt, type_="bearer")

    def create_basic_auth(self, login: str, password: str) -> str:
        creds = f"{login}:{password}".encode(self.encoding)
        basic = base64.b64encode(creds).decode(self.encoding)
        return f"Basic {basic}"

    def decode_basic_auth(self, basic: str) -> tuple[str, str] | None:
        schema, basic = basic.split(" ", maxsplit=1)
        if schema.lower() != "basic":
            return None
        decoded = base64.urlsafe_b64decode(basic).decode(self.encoding)
        username, password = decoded.split(":", maxsplit=1)
        return username, password
