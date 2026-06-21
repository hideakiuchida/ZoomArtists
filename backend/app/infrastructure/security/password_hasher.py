"""Bcrypt implementation of the PasswordHasher port."""

import bcrypt

from app.application.ports import PasswordHasher


def _to_bytes(password: str) -> bytes:
    # bcrypt only considers the first 72 bytes; truncate to avoid ValueError.
    return password.encode("utf-8")[:72]


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return bcrypt.hashpw(_to_bytes(password), bcrypt.gensalt()).decode("utf-8")

    def verify(self, plain: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(_to_bytes(plain), hashed.encode("utf-8"))
        except ValueError:
            return False
