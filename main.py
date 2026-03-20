from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import shutil
import os

# ------------------------------------------------------------
# CREATE APP
# THIS OBJECT MUST EXIST FOR UVICORN
# ------------------------------------------------------------
app = FastAPI()


# ------------------------------------------------------------
# HOME ROUTE (TEST)
# ------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>SnapMind Running</h1>"


# ------------------------------------------------------------
# TEST ROUTE
# ------------------------------------------------------------
@app.get("/test")
def test():
    return {"status": "ok"}
