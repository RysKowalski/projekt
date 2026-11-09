class Encryption:
    def __init__(self, key: str | None = None):
        self.key: str | None = key

    def encrypt_b(self, data: bytes):
        return data

    def decrypt_b(self, data: bytes):
        return data
