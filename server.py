import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

from database import Database, User, UserInDb
from declarations import Bitmap

# to get a string like this run:
# openssl rand -hex 32
load_dotenv()
SECRET_KEY: str | None = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    raise LookupError('environment variable "SECRET_KEY" is not present')

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class RegisterData(BaseModel):
    username: str
    password: str


db: Database = Database()

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()
app.frontend("/", directory="frontend")


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return password_hash.hash(password)


def authenticate_user(username: str, password: str) -> User | None:
    user: UserInDb | None = db.get_user(username)
    if not user:
        return
    if not verify_password(password, user.password_hash):
        return
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserInDb | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user: UserInDb | None = db.get_user(username)
    return user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


@app.post("/ttf")
def get_ttf(
    font: Bitmap, _: Annotated[User, Depends(get_current_user)]
) -> FileResponse:
    print(font)
    return FileResponse("aria.ttf", filename="font.ttf")


@app.post("/register")
def register(data: RegisterData) -> None:
    if db.get_user(data.username) is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"user '{data.username}' already exists"
        )

    db.add_user(data.username, get_password_hash(data.password))
