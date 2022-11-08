from fastapi import FastAPI, Request, Form, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from pyngrok import ngrok as ngrokModule
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
ngrokLink = ""


def setNgrok():
    global ngrokLink
    if bool(config["ngrok"]["on"]) and config["ngrok"]["token"] != "":
        ngrokModule.set_auth_token(config["ngrok"]["token"])
        ngrokLink = "<tr><th>%s</th></tr>"%ngrokModule.connect(config["port"])
        print(ngrokLink)
    else:
        ngrokLink = ""
        ngrokModule.kill()
def render_templates(index_html, data):
    for i in data:
        index_html = index_html.replace(f"/*{i}*/",str(data[i]))
    return index_html

def genAdminToken():
    adminToken = ""
    for i in range(20):
        adminToken += str(random.randrange(0,10))
    return adminToken
radminToken = genAdminToken()
setNgrok()

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
    admin_html = open(cur_path_of_py_file+"/templates/admin-tem.txt").read()
    index_html = open(cur_path_of_py_file+"/templates/admin-login.txt").read()
    print(radminToken)
    return HTMLResponse(render_templates(admin_html, {"content":index_html}))

@app.post("/admin")
def admin_login(response:Response,adminToken:str = Form("")):
    print(adminToken)
    if adminToken == radminToken:
        response.set_cookie(key="adminToken",value=adminToken)
        return "สำเร็จ"
    response.delete_cookie(key="adminToken")
    return "Tokenผิดพลาด"


@app.get("/admin/config")
def config_html(adminToken  = Cookie(None,alias="adminToken")):
    if adminToken != radminToken:
        return HTMLResponse(
        """
        <script>
            window.location.href = "/admin"
        </script>
        """
        )
    admin_html = open(cur_path_of_py_file+"/templates/admin-tem.txt").read()
    index_html = open(cur_path_of_py_file+"/templates/admin-config.txt").read()
    data_cf = {
        "port":config["port"],
        "path":config["parent path"],
        "home":config["template"]["home"],
        "withGsheetCheck":"checked" if config["with_gform_and_gsheet"]["on"] else "",
        "gFormLink":config["with_gform_and_gsheet"]["form_link"],
        "sheetLink":config["with_gform_and_gsheet"]["sheet_link"],
        "sheetLinkCSV":config["with_gform_and_gsheet"]["csv_link"],
        "ngrokDes":"สำหรับแชร์ Localhost",
        "ngrokLink":ngrokLink,
        "ngrokCheck": "checked" if config["ngrok"]["on"] else "",
        "ngrokToken":config["ngrok"]["token"]
    }
    index_html = render_templates(admin_html, {"content":render_templates(index_html, data_cf)})
    return HTMLResponse(index_html)

@app.post("/admin/config")
def set_config(
        path:str = Form(""),
        home:str = Form(""),
        storageType:str = Form(""), sheetLink:str  = Form(""), sheetLinkCSV:str = Form(""),
        gFormLink:str = Form(""),
        ngrok:bool = Form(""), ngrokToken:str = Form("")):
    global config, ngrokLink
    #config หลัก
    config_js = open(cur_path_of_py_file+"/data/config.json","w")
    config["parent path"] = path
    config["template"]["home"] = home
    #config ประเภทที่เก็บข้อมูล
    if storageType == "local":
        config["with_gform_and_gsheet"]["on"] = 0
    else:
        config["with_gform_and_gsheet"]["on"] = 1
    #config ngrok
    if ngrok:
        config["ngrok"]["on"] = 1
        config["ngrok"]["token"] = ngrokToken
        setNgrok()
    else:
        config["ngrok"]["on"] = 0
        config["ngrok"]["token"] = ""
        setNgrok()
    config_js.write(json.dumps(config))
    config_js.close()
    return HTMLResponse("""
    <script>
        window.location.href = "./config"
    </script>
    """)

uvicorn.run(app, port=int(config["port"]))
