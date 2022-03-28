from typing import Dict
import secrets
from otsapp.dtos import SecretData


class SecretKeeper:
    __secrets: Dict[str, SecretData] = {}

    def add_secret(self, data: SecretData) -> str:
        key = secrets.token_urlsafe()
        self.__secrets[key] = data
        return key

    def is_key_valid(self, key: str) -> bool:
        return key in self.__secrets

    def get_secret(self, key: str) -> SecretData:
        return self.__secrets[key]

    def remove_secret(self, key: str):
        del self.__secrets[key]
