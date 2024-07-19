"""Models for the ANS API token."""

from pathlib import Path

from pydantic import BaseModel, EmailStr, Field

from utils import load_json_file


class ReadConfig(BaseModel):
    """the ReadConfig Data class."""

    config: dict[str, str] = load_json_file(Path("..", "config", "token.json"))


class UrlToken(BaseModel):
    """the authentification URL class."""

    url_token: str = ReadConfig().config["query_token_url"]


class HeaderToken(BaseModel):
    """the authentification header class."""

    content_type: str = Field(ReadConfig().config["content_type"], alias="Content-Type")


class TokenData(BaseModel):
    """the TokenData class."""

    grant_type: str = "password"
    client_id: str = ReadConfig().config["client_id"]
    username: EmailStr
    password: str
    refresh_token: str = ReadConfig().config["refresh_token"]
