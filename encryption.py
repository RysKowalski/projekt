from cryptography.fernet import Fernet


class Encryption:
    def __init__(self, key: str = Fernet.generate_key().decode()) -> None:
        self.fernet: Fernet = Fernet(key)

    def encrypt_b(self, data: bytes) -> bytes:
        return self.fernet.encrypt(data)

    def decrypt_b(self, data: bytes) -> bytes:
        return self.fernet.decrypt(data)

    def encrypt_s(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt_s(self, data: str) -> str:
        return self.fernet.decrypt(data).decode()


if __name__ == "__main__":
    enc = Encryption("Ilx4oRhvR_gzjImgLZAZlrGOiNA8rPmYgn1FpLXcnl0=")

    s = "string"
    b = "bytes".encode()
    print(f"string={s}, bytes={b}")

    es = enc.encrypt_s(s)
    eb = enc.encrypt_b(b)
    print(f"encString={es}, encBytes={eb}")

    ds = enc.decrypt_s(es)
    db = enc.decrypt_b(eb)
    print(f"decString={ds}, decBytes={db}")
