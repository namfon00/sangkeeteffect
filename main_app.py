from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
import json

app = FastAPI()
#หาpathปัจจุบันของโปรเจค
cur_path_of_py_file = __file__[:__file__.rfind("\\")].replace("\\", "/")

#อ่านไฟล์ config
config = json.loads(open(cur_path_of_py_file+"/data/config.json").read())

tem_path = config["templates path"] if config["templates path"] != "" else cur_path_of_py_file

@app.get("/")
def home():
    index_html = open(tem_path+config["home path"]).read()
    return HTMLResponse(index_html.replace("/*text*/","Hello"))

@app.get("/search")
def search(keyword:str):
    index_html = open(tem_path+config["home path"]).read()
    return HTMLResponse(index_html.replace("/*text*/",keyword))

uvicorn.run(app,port=config["port"])
