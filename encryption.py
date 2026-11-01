import hashlib

def hash(password:str):
    # .encode() turns string into bytes
    # .hexdigest() turns bytes to text in hexadecimal systen
    return hashlib.sha256(password.encode()).hexdigest()

def is_password_correct(password:str, hashed_password:str) -> bool:
    return hash(password) == hashed_password
