from fastapi import FastAPI
from fastapi.responses import Response, FileResponse, HTMLResponse
import uvicorn
import json
import os
import requests
import random
import platform
from modules import KhunSangkeetE_Admin, KhunSangkeetE_User

def setConfigFile():
    """create file config สร้างไฟล์config"""
    global cur_path_of_py_file
    open(cur_path_of_py_file+"/data/config.json", "w").write("""{"host": "localhost", "port": "8080", "parent path": "./", "template": {"home": "/templates/home.txt", "add_sound": "/templates/add_sound.txt", "info": "/templates/info.txt", "err404": "/templates/404.txt"}, "ngrok": {"on": 0, "token": ""}, "local_storage": {"on": 1, "sound data": "/data/sound_data.json", "sound path": "/data/sound", "cover path": "/cover"}, "with_gform_and_gsheet": {"on": 0, "form_link": "https://forms.gle/TCcyW8BmLQJmcbtC8", "sheet_link": "https://docs.google.com/spreadsheets/d/1OU-fN7NAYX68PAAeAm-W3ppEa3eFSE0dtsL-Glxn0ZI/edit", "csv_link": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTcV3Nob9Hk2j2eKRQpP3IaYZ1UFCPVQ9YGdmnAzl5TorIi7DhDcA5e7EJWQCI_8nXkuuqx5l5YdBwY/pub?gid=203295964&single=true&output=csv"}}""")
    print("set config file")
def gen_AdminToken_and_ItemId(_type:str = "token"):
    """Generate Token for Login and Generate Id for Item
    สร้างTokenในการใช้Login และสร้าง Id สำหรับข้อมูล"""
    adminToken = ""
    for _ in range(20):
        i = random.randint(0,4)
        char = [
            [chr(c) for c in range(ord('A'), ord('Z'))],
            ['!', '@', '#', '$', '%', '&', '-', '+'],
            [chr(c) for c in range(ord('a'), ord('z'))]
        ]
        if i == 0:
            adminToken += random.choice(char[0])
        elif i == 1:
            adminToken += random.choice(char[1]) if _type == "token" else str(random.randrange(0, 10))
        elif i == 2:
            adminToken += random.choice(char[2])
        else:
            adminToken += str(random.randrange(0, 10))
    if _type == "token":
        print(adminToken)
        sent_token_to_discord(token=adminToken)
    return adminToken
def render_templates(index_html:str = "", data:dict = {}, path:str = ""):
    """Render templates
        Usage วิธีใช้
        /*name*/ in html for point position where should replace by value
        วาง /*n...*/ เพื่อรระบุตำแหน่งที่ะแทนค่า
        (index_html:str, data:dict, [path:str])
        sample
            render_templates("<h1>/*head1*/</h1>",{"head1":"Hello"})
            result : <h1>Hello</h1>
    """
    #ช้ทดแทน Module templating ของ Fastapi ที่เกิดปัญหากับภาษาไทย
    if path != "":
        index_html = open(path, "r", encoding="utf-8").read()
    for i in data:
        index_html = index_html.replace(f"/*{i}*/", str(data[i]))
    return index_html
def redirect_url(url_path = "/"):
    """redirect_url"""
    #ใช้ทดแทน Module RedirectResponse ของ Fastapi ที่เกิดปัญหา เปลี่ยนเส้นทางของคุณบ่อยเกินไป(ERR_TOO_MANY_REDIRECTS)
    return f"""<script> window.location.href = "{url_path}" </script>"""
def alert(icon:str = "info" ,mss:str = ""):
    if "wrong" in mss.lower() or "error" in mss.lower():
        icon = "error"
    elif "success" in mss.lower():
        icon = "success"
    if mss == "" or mss == None:
        return ""
    result = """ 
            Toast.fire({
                icon: '%s',
                title: '%s',
                color: '%s'
                });
            """%(icon, mss, "var(--bs-danger)" if icon == "error" else "var(--bs-success)" if icon == "success" else "")
    return result
def sent_token_to_discord(token="", ngrok_link=""):
    if  not config["send_token_to_discord"]["on"]:
        return ""
    if config["send_token_to_discord"]["webhook_url"] != "":
        requests.post(config["send_token_to_discord"]["webhook_url"],
        json={
                "content": "",
                "embeds": [
                    {
                    "title": "Your TokenKey",
                    "description": "Token : %s "%token if token != "" else ngrok_link,
                    "color": 7559423 if token != "" else 5199043,
                    "footer":{
                        "text": "%s %s"
                        %("Running From : " + platform.platform() if config["send_token_to_discord"]["show_os"] == 1 else " ",
                        "| Ip : "+str(requests.get("https://api.ipify.org").content, encoding="utf-8") if config["send_token_to_discord"]["show_ip"] == 1 else "")
                    }
                    }
                ],
                "username": "KhunSangkeet E-Admin",
                "attachments": []
            })


app = FastAPI()
KhunSangkeetE_Admin.app = app

if __file__.find("\\") != -1:
    # Windows case กรณีใช้ Windows
    cur_path_of_py_file = __file__[:__file__.rfind("\\")].replace("\\", "/")
else:
    # Linux / Mac case กรณีใช้ Linux / Mac
    cur_path_of_py_file = __file__[:__file__.rfind("/")]

config = ""
try:
    config = json.loads(
        open(cur_path_of_py_file+"/data/config.json", "r", encoding="utf-8").read())
    if config == "":
        setConfigFile()
        config = json.loads(
            open(cur_path_of_py_file+"/data/config.json", "r", encoding="utf-8").read())
except:
    setConfigFile()
    config = json.loads(
        open(cur_path_of_py_file+"/data/config.json", "r", encoding="utf-8").read())        

parent_path = config["parent path"] if config["parent path"] != "./" else cur_path_of_py_file

KhunSangkeetE_Admin.cur_path_of_py_file = cur_path_of_py_file
KhunSangkeetE_Admin.config = config
KhunSangkeetE_Admin.adminTemPath = cur_path_of_py_file+"/admin_templates/admin-tem.txt"
KhunSangkeetE_Admin.admin_redirect = redirect_url("/admin")
KhunSangkeetE_Admin.redirect = redirect_url
KhunSangkeetE_Admin.ngrok = bool(config["ngrok"]["on"])
KhunSangkeetE_Admin.parent_path = parent_path
KhunSangkeetE_Admin.radminToken = gen_AdminToken_and_ItemId()
KhunSangkeetE_Admin.render_templates = render_templates
KhunSangkeetE_Admin.alert = alert
KhunSangkeetE_Admin.serverOS = platform.system()
KhunSangkeetE_Admin.adminSys()
app = KhunSangkeetE_Admin.app

KhunSangkeetE_User.app = app
KhunSangkeetE_User.config = config
KhunSangkeetE_User.parent_path = parent_path
KhunSangkeetE_User.render_templates = render_templates
KhunSangkeetE_User.genToken = gen_AdminToken_and_ItemId
KhunSangkeetE_User.redirect = redirect_url
KhunSangkeetE_User.userSys()
app = KhunSangkeetE_User.app

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.get("/favicon.ico")
def icon():
    return "https://media.discordapp.net/attachments/1036704934432886876/1037321689073188894/cropped-it-logo.png"

uvicorn.run(app, host=config["host"], port=int(config["port"]))
