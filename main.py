from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import shutil
import os

# Import your pipeline
from processor_pipeline import process_image

# ------------------------------------------------------------
# CREATE APP (THIS IS WHAT UVICORN LOOKS FOR)
# ------------------------------------------------------------
app = FastAPI()


# ------------------------------------------------------------
# HOME PAGE (MOBILE UI)
# ------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html") as f:
        return f.read()


# ------------------------------------------------------------
# SINGLE IMAGE (SCREENSHOT)
# ------------------------------------------------------------
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)

    path = f"uploads/{file.filename}"

    # Save uploaded file
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"Processing: {path}")

    # Process image (OCR → note)
    process_image(path)

    return {"status": "done"}


# ------------------------------------------------------------
# MULTIPLE IMAGES (IMPORT FEATURE)
# ------------------------------------------------------------
@app.post("/upload-multiple/")
async def upload_multiple(files: list[UploadFile] = File(...)):

    os.makedirs("uploads", exist_ok=True)

    for file in files:

        path = f"uploads/{file.filename}"

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        process_image(path)

    return {"status": "batch done"}
