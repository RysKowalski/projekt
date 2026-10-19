from fastapi import FastAPI
from fastapi.responses import FileResponse
from declarations import Bitmap


app: FastAPI = FastAPI()
app.frontend("/", directory="frontend")


@app.post("/ttf")
def get_ttf(font: Bitmap) -> FileResponse:
    print(font)
    return FileResponse("aria.ttf", filename="font.ttf")


@app.post("/login")
def login(username: str, password: str) -> None:
    return


@app.post("/register")
def register(username: str, password: str) -> None:
    return
