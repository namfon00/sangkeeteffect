from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn
import json

app = FastAPI()
#หาpathปัจจุบันของโปรเจค
cur_path_of_py_file = __file__[:__file__.rfind("\\")].replace("\\", "/")

#อ่านไฟล์ config
config = json.loads(open(cur_path_of_py_file+"/data/config.json").read())

tem_path = config["templates path"] if config["templates path"] != "./" else cur_path_of_py_file

@app.get("/")
def home():
    index_html = open(tem_path+config["home path"]).read()
    return HTMLResponse(index_html.replace("/*text*/","Hello"))

@app.get("/search")
def search(keyword:str):
    index_html = open(tem_path+config["home path"]).read()
    return HTMLResponse(index_html.replace("/*text*/",keyword))

@app.get("/admin/config")
def config_html():
    index_html = open(cur_path_of_py_file+"/templates/admin-config.txt").read()
    data_cf = {
        "port":config["port"],
        "path":config["templates path"],
        "home":config["home path"]
    }
    for i in data_cf:
        index_html = index_html.replace(f"/*{i}*/",str(data_cf[i]))
    return HTMLResponse(index_html)

@app.post("/admin/config")
def set_config(port:int = Form(),path:str = Form(),home:str= Form()):
    global config
    config_js = open(cur_path_of_py_file+"/data/config.json","w")
    config["port"] = port
    config["templates path"] = path
    config["home path"] = home
    config_js.write(json.dumps(config))
    config_js.close()
    return HTMLResponse("""
    <script>
        window.location.href = "./config"
    </script>
    """)

uvicorn.run(app,port=config["port"])
