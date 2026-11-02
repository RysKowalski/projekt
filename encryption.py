import hashlib



class Encryption:
    def __init__(key=None):
        pass
    def encrypt(text: str):
        pass
    def decrypt(text: str):
        pass
    def get_key():
        pass

    @staticmethod
    def hash(password:str):
        # .encode() turns string into bytes
        # .hexdigest() turns bytes to text in hexadecimal systen
        return hashlib.sha256(password.encode()).hexdigest()


