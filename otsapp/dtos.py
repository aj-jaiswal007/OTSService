from pydantic import BaseModel


class SecretData(BaseModel):
    secret: str
