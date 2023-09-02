import re

from pydantic import BaseModel
from pydantic import field_validator


class Token(BaseModel):
    jwt: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str

    @field_validator('access_token', 'refresh_token')
    def validate_jwt(cls, value):
        jwt_pattern = re.compile(
            r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*$'
        )
        if not jwt_pattern.match(value):
            raise ValueError('Invalid JWT format')
        return value


class TokenPayloadBase(BaseModel):
    sub: str
    exp: str


class TokenUserPayload(TokenPayloadBase):
    fresh: str


class TokenEmailVerifyPayload(TokenPayloadBase):
    _type: str


class TokenRetreivePasswordPayload(TokenPayloadBase):
    _type: str
