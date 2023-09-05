import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    secret_key: str=os.getenv("JWT_SECRET")
    token_duration: int=os.getenv("ACCESS_TOKEN_DURATION")
    algorithm: str=os.getenv("ALGORITHM")

