import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


def generate_salt():
    # Generate a secure random salt
    return os.urandom(16)


def derive_key(password: str, salt: bytes) -> bytes:
    # Derive a secure encryption key from a password using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_data(data: bytes, key: bytes) -> bytes:
    # Encrypt data using Fernet symmetric encryption
    f = Fernet(key)
    return f.encrypt(data)


def decrypt_data(token: bytes, key: bytes) -> bytes:
    # Decrypt data using Fernet symmetric encryption
    f = Fernet(key)
    return f.decrypt(token)
