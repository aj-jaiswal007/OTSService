from typing import Optional
from pydantic import BaseModel


class SecretData(BaseModel):
    secret: str
    passphrase: Optional[str]
