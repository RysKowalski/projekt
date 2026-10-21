from fastapi import FastAPI
from fastapi.responses import FileResponse


BitMap = type


app: FastAPI = FastAPI()
app.frontend("/", directory="frontend")


@app.post("/ttf")
def get_ttf(fontBitMap: BitMap) -> FileResponse:
    print(fontBitMap)
    return FileResponse("aria.ttf")
