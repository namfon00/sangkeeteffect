from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/")
def index():
    return HTMLResponse("<h1>sawasdeejaaaa</h1>")

@app.get("/567")
def index():
    return HTMLResponse("<h1>ฟหกด</h1>")

uvicorn.run(app)