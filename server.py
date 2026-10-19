from fastapi import FastAPI
from fastapi.responses import FileResponse


Char = list[list[bool]]
Bitmap = dict[str, Char]

app: FastAPI = FastAPI()
app.frontend("/", directory="frontend")


@app.post("/ttf")
def get_ttf(font: Bitmap) -> FileResponse:
    print(font)
    return FileResponse("aria.ttf", filename="font.ttf")
