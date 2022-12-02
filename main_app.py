from fastapi import FastAPI
import uvicorn
import json
import os
import random
from modules import KhunSangkeetE_Admin, KhunSangkeetE_User

def setConfigFile():
        global cur_path_of_py_file
        open(cur_path_of_py_file+"/data/config.json", "w").write("""{"host": "localhost", "port": "8080", "parent path": "./", "template": {"home": "/templates/home.txt"}, "ngrok": {"on": 0, "token": "2E9lFpayxjyEXqPEl1fCCiibujh_7S1itcMv8pfBofs5L3iWG"}, "local_storage": {"on": 0, "sound data": "/data/sound_data.json", "sound path": "/sound", "cover path": "/cover"}, "with_gform_and_gsheet": {"on": 1, "form_link": "https://forms.gle/TCcyW8BmLQJmcbtC8", "sheet_link": "https://docs.google.com/spreadsheets/d/1OU-fN7NAYX68PAAeAm-W3ppEa3eFSE0dtsL-Glxn0ZI/edit", "csv_link": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTcV3Nob9Hk2j2eKRQpP3IaYZ1UFCPVQ9YGdmnAzl5TorIi7DhDcA5e7EJWQCI_8nXkuuqx5l5YdBwY/pub?gid=1384870553&single=true&output=csv"}}""")
        print("set config file")
def genAdminToken():
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
            adminToken += random.choice(char[1])
        elif i == 2:
            adminToken += random.choice(char[2])
        else:
            adminToken += str(random.randrange(0, 10))
    print(adminToken)
    return adminToken
def render_templates(index_html:str, data:dict):
        for i in data:
            index_html = index_html.replace(f"/*{i}*/", str(data[i]))
        return index_html

app = FastAPI()
KhunSangkeetE_Admin.app = app

if __file__.find("\\") != -1:
    cur_path_of_py_file = __file__[:__file__.rfind("\\")].replace("\\", "/")
else:
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
KhunSangkeetE_Admin.admin_redirect = """
                                    <script>
                                        window.location.href = "/admin"
                                    </script>
                                    """


KhunSangkeetE_Admin.ngrok = bool(config["ngrok"]["on"])
KhunSangkeetE_Admin.parent_path = parent_path
KhunSangkeetE_Admin.radminToken = genAdminToken()
KhunSangkeetE_Admin.render_templates = render_templates
KhunSangkeetE_Admin.adminSys()
app = KhunSangkeetE_Admin.app

KhunSangkeetE_User.app = app
KhunSangkeetE_User.config = config
KhunSangkeetE_User.parent_path = parent_path
KhunSangkeetE_User.render_templates = render_templates
KhunSangkeetE_User.userSys()
app = KhunSangkeetE_User.app

uvicorn.run(app, host=config["host"], port=int(config["port"]))