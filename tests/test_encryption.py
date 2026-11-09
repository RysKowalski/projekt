from cryptography.fernet import Fernet

from encryption import Encryption


def test_encrypt_decrypt() -> None:
    e = Encryption()
    data: bytes = "text".encode()

    encrypted: bytes = e.encrypt(data)
    decrypted: bytes = e.decrypt(encrypted)

    assert decrypted == data


def test_encrypt_decrypt_str() -> None:
    e = Encryption()
    text: str = "text"

    encrypted: bytes = e.encrypt(text)
    decrypted: str = e.decrypt_str(encrypted)

    assert isinstance(decrypted, str)
    assert decrypted == text


def test_same_key_decrypts() -> None:
    key: str = Fernet.generate_key().decode()
    e1 = Encryption(key)
    text: str = "text"

    encrypted: bytes = e1.encrypt(text)
    del e1
    e2 = Encryption(key)
    decrypted: str = e2.decrypt_str(encrypted)

    assert decrypted == text


def test_different_key_cant_decrypt() -> None:
    key1: str = Fernet.generate_key().decode()
    key2: str = Fernet.generate_key().decode()
    e1 = Encryption(key1)
    e2 = Encryption(key2)
    text: str = "text"
    decrypted: str | None = None

    encrypted: bytes = e1.encrypt(text)
    try:
        decrypted = e2.decrypt_str(encrypted)
    except Exception:
        pass

    assert text != decrypted
