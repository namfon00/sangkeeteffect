from fastapi import FastAPI, Request, Form, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn
import json
import random
import time

app = FastAPI()
#หาpathปัจจุบันของโปรเจค
cur_path_of_py_file = __file__[:__file__.rfind("\\")].replace("\\", "/")

#อ่านไฟล์ config
config = json.loads(open(cur_path_of_py_file+"/data/config.json").read())

tem_path = config["parent path"] if config["parent path"] != "./" else cur_path_of_py_file
ngrok = bool(config["ngrok"]["on"])

def render_templates(index_html, data):
    for i in data:
        index_html = index_html.replace(f"/*{i}*/",str(data[i]))
    return index_html
def genAdminToken():
    adminToken = ""
    for i in range(20):
        adminToken += str(random.randrange(0,10))
    return adminToken
radminToken = "1234"#genAdminToken()

@app.get("/")
def home():
    index_html = open(tem_path+config["template"]["home"]).read()
    return HTMLResponse(index_html.replace("/*text*/","Hello"))

@app.get("/search")
def search(keyword:str):
    index_html = open(tem_path+config["template"]["home"]).read()
    return HTMLResponse(index_html.replace("/*text*/",keyword))

@app.get("/admin")
def admin():
    index_html = open(cur_path_of_py_file+"/templates/admin-login.html").read()
    print(radminToken)
    return HTMLResponse(index_html)

@app.post("/admin")
def admin_login(response:Response,adminToken:str = Form("")):
    print(adminToken)
    if adminToken == radminToken:
        response.set_cookie(key="adminToken",value=adminToken)
        return ""
    response.delete_cookie(key="adminToken")
    return HTMLResponse(
    """
    <script>
        window.location.href = "/admin?wrongtoken=True"
    </script>
    """
    )


@app.get("/admin/config")
def config_html(adminToken  = Cookie(None,alias="adminToken")):
    print(adminToken,radminToken)
    if adminToken != radminToken:
        return HTMLResponse(
        """
        <script>
            window.location.href = "/admin"
        </script>
        """
        )
    index_html = open(cur_path_of_py_file+"/templates/admin-config.txt").read()
    data_cf = {
        "port":config["port"],
        "path":config["parent path"],
        "home":config["template"]["home"],
        "ngrokDes":"สำหรับแชร์ Localhost",
        "ngrokCheck": "checked" if config["ngrok"]["on"] else "",
        "ngrokToken":config["ngrok"]["token"]
    }
    index_html = render_templates(index_html, data_cf)
    return HTMLResponse(index_html)

@app.post("/admin/config")
def set_config(
        port:int = Form(""),
        path:str = Form(""),
        home:str = Form(""),
        ngrok:bool = Form(""), ngrokToken:str = Form("")):
    global config
    config_js = open(cur_path_of_py_file+"/data/config.json","w")
    config["port"] = port
    config["parent path"] = path
    config["template"]["home"] = home
    config["ngrok"]["on"] = 1 if ngrok else 0
    if config["ngrok"]["on"] == 1:
        config["ngrok"]["token"] = ngrokToken
    config_js.write(json.dumps(config))
    config_js.close()
    return HTMLResponse("""
    <script>
        window.location.href = "./config"
    </script>
    """)

uvicorn.run(app,port=config["port"])
