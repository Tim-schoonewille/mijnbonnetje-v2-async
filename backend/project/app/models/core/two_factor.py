import random
from uuid import uuid4
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field


def generat_otp() -> str:
    otp = random.randint(100_000, 999_999)
    return str(otp)


class TwoFactorSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    code: str = Field(default_factory=generat_otp)
    user_id: int | UUID
    consumed: bool = False
