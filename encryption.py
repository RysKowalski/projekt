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


if __name__ == "__main__":
    enc = Encryption("Ilx4oRhvR_gzjImgLZAZlrGOiNA8rPmYgn1FpLXcnl0=")

    s = "string"
    b = "bytes".encode()
    print(f"string={s}, bytes={b}")

    es = enc.encrypt(s)
    eb = enc.encrypt(b)
    print(f"encString={es}, encBytes={eb}")

    ds = enc.decrypt(es).decode()
    db = enc.decrypt(eb)
    print(f"decString={ds}, decBytes={db}")
