from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
#หาpathปัจจุบันของโปรเจค
cur_path_of_py_file = __file__[:__file__.rfind("\\")].replace("\\", "/")


@app.get("/")
def home():
    index_html = open(cur_path_of_py_file+"/templates/home.html").read()
    return HTMLResponse(index_html.replace("/*text*/","Hello"))

@app.get("/search")
def search(keyword:str):
    index_html = open(cur_path_of_py_file+"/templates/home.html").read()
    return HTMLResponse(index_html.replace("/*text*/",keyword))

uvicorn.run(app)
