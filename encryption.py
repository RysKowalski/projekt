from cryptography.fernet import Fernet


class Encryption:
    def __init__(self, key: str = Fernet.generate_key().decode()) -> None:
        self.fernet: Fernet = Fernet(key)

    def encrypt(self, data: bytes | str) -> bytes:
        if isinstance(data, str):
            return self.fernet.encrypt(data.encode())
        return self.fernet.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        return self.fernet.decrypt(data)

    def decrypt_str(self, data: bytes) -> str:
        return self.decrypt(data).decode()
