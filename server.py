from fastapi import FastAPI
from fastapi.responses import FileResponse
from declarations import Char, Bitmap


app: FastAPI = FastAPI()
app.frontend("/", directory="frontend")


@app.post("/ttf")
def get_ttf(font: Bitmap) -> FileResponse:
    print(font)
    return FileResponse("aria.ttf", filename="font.ttf")
