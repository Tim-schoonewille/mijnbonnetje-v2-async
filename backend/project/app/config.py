import logging
from enum import Enum
from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pydantic import EmailStr


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    ENVIRONMENT: str = "dev"
    TESTING: bool = bool(0)
    ID_UUID: bool = False
    URL_PREFIX: str = ""
    APP_FQDN: str = "http://frontend.mijnbonnetje.lan:3000/"
    TRAFFIC_LOGGING: bool = False
    DEFAULT_API_CALL_LIMIT: int = 30
    TWO_FACTOR_VERIFICATION_LINK: str = APP_FQDN + "auth/twofactor/"

    # Database
    DB_ASYNC_URL: str
    DB_SYNC_URL: str
    DB_SQL_ECHO: bool = False
    DB_TEST_ASYNC_URL: str
    DB_TEST_SYNC_URL: str

    # TOKEN
    ACCESS_TOKEN_COOKIE_NAME: str = "access_token"
    REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    ACCES_TOKEN_EXPIRES: int = 5 * 60
    REFRESH_TOKEN_EXPIRES: int = 60 * 60 * 24
    EMAIL_TOKEN_EXPIRES: int = 15 * 60
    PASSWORD_TOKEN_EXPIRES: int = 5 * 60
    SECRET_KEY: str = "supersuperdupersecret..."
    ALGORITHM: str = "HS256"

    # cookie settings
    DOMAIN: str = "mijnbonnetje.lan"
    COOKIE_SECURE: bool = False
    SAME_SITE: str = 'strict'

    # REDIS
    REDIS_PASSWORD: str
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_LOCKOUT_TIME: int = 30
    REDIS_LOGIN_PREFIX: str = "login_attempts_user"
    CACHE_EXPIRATION_TIME: int = 600

    # MONGO
    MONGO_DB_URL: str
    MONGO_DB_DB: str
    MONGO_DB_TESTDB: str
    MONGO_COLLECTION: str = "userRequestLog"
    API_CALL_LOG_COLLECTION: str = "userApiCallLog"
    API_TRAFFIC_COLLECTION: str = "apiTrafficCollection"

    # Email
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    MAIL_FROM_NAME: str = "noreply@mijnbonnetje.nl"
    MAIL_FROM_EMAIL: EmailStr = "tim@flowerofmine.nl"

    # TwoFactor
    OTP_CACHE_PREFIX: str = "OTP_"

    # Static Files
    STATIC_FOLDER: str = "/public/"
    MAX_FILE_SIZE: int = 4
    ALLOWED_FILE_TYPES: list = ["image/jpeg", "image/png"]

    # OpenAI
    OPENAI_API_KEY: str


@lru_cache()
def get_settings() -> Settings:
    log.info("[+] Loading config settings from the environment...")
    return Settings()  # type: ignore


CACHED_ITEM_PREFIX = "cached_result_"

ROUTERS_ROOT_PATH = "app/routers"
ROUTERS_EXCLUDE_FOLDERS = ["__pycache__"]
ROUTERS_EXCLUDE_FILES = ["__init__.py"]


class CachedItemPrefix(str, Enum):
    ITEM = f"{CACHED_ITEM_PREFIX}item_"
    USER = f"{CACHED_ITEM_PREFIX}user_"
    TIER = f"{CACHED_ITEM_PREFIX}tier_"
    RECEIPT = f'{CACHED_ITEM_PREFIX}receipt_'
    RECEIPT_ENTRY = f'{CACHED_ITEM_PREFIX}receipt_entry_'
    PROXY_IP = f'{CACHED_ITEM_PREFIX}proxy_ip_'


PROXY_IPS = ['2.1.1.1:80', '3.2.2.2:80', '4.3.3.3:80', '5.4.4.4:80']

settings = get_settings()
