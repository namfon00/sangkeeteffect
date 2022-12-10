from fastapi import FastAPI
import uvicorn
import json
import os
from modules import KhunSangkeetE_Admin, KhunSangkeetE_User, FunctionForModule, CheckRequireFile
from modules import KhunSangkeetE_Admin_SubSystem

app = FastAPI(
    openapi_url = None,
    docs_url = None,
    redoc_url = None
)

if __file__.find("\\") != -1:
    # Windows case กรณีใช้ Windows
    cur_path_of_py_file = __file__[:__file__.rfind("\\")].replace("\\", "/")
else:
    # Linux / Mac case กรณีใช้ Linux / Mac
    cur_path_of_py_file = __file__[:__file__.rfind("/")]

config = {}
FunctionForModule.cur_path_of_py_file = cur_path_of_py_file


if CheckRequireFile.checkSys():
    if CheckRequireFile.limit_option:
        print("\x1b[38;5;226m====================  App Start\x1b[38;5;196m With Limited Option    ====================")
    else:
        print("\x1b[38;5;226m======================================  App Start  ======================================")
    config = json.loads(open(cur_path_of_py_file+"/data/config.json", "r", encoding="utf-8").read())
    
    FunctionForModule.config = config
    parent_path = config["parent path"] if config["parent path"] != "./" else cur_path_of_py_file

    KhunSangkeetE_Admin.app = app
    KhunSangkeetE_Admin.cur_path_of_py_file = cur_path_of_py_file
    KhunSangkeetE_Admin.config = config
    KhunSangkeetE_Admin.adminTemPath = cur_path_of_py_file+"/admin_templates/admin-tem.txt"
    KhunSangkeetE_Admin.admin_redirect = FunctionForModule.redirect_url("/admin")
    KhunSangkeetE_Admin.redirect = FunctionForModule.redirect_url
    KhunSangkeetE_Admin.ngrok = bool(config["ngrok"]["on"])
    KhunSangkeetE_Admin.parent_path = parent_path
    KhunSangkeetE_Admin.radminToken = FunctionForModule.gen_AdminToken_and_ItemId()
    KhunSangkeetE_Admin.render_templates = FunctionForModule.render_templates
    KhunSangkeetE_Admin.alert = FunctionForModule.alert
    KhunSangkeetE_Admin.limit_option = CheckRequireFile.limit_option
    KhunSangkeetE_Admin.send_to_discord = FunctionForModule.send_to_discord
    KhunSangkeetE_Admin.adminSys()
    app = KhunSangkeetE_Admin.app

    KhunSangkeetE_Admin_SubSystem.app = app
    KhunSangkeetE_Admin_SubSystem.radminToken = KhunSangkeetE_Admin.radminToken
    KhunSangkeetE_Admin_SubSystem.admin_redirect = FunctionForModule.redirect_url("/admin")
    KhunSangkeetE_Admin_SubSystem.cur_path_of_py_file = cur_path_of_py_file
    KhunSangkeetE_Admin_SubSystem.parent_path = parent_path
    KhunSangkeetE_Admin_SubSystem.config = config
    KhunSangkeetE_Admin_SubSystem.adminTemPath = cur_path_of_py_file+"/admin_templates/admin-tem.txt"
    KhunSangkeetE_Admin_SubSystem.render_templates = FunctionForModule.render_templates
    KhunSangkeetE_Admin_SubSystem.redirect = FunctionForModule.redirect_url
    KhunSangkeetE_Admin_SubSystem.alert = FunctionForModule.alert
    KhunSangkeetE_Admin_SubSystem.adminSubSys()
    app = KhunSangkeetE_Admin_SubSystem.app

    KhunSangkeetE_User.app = app
    KhunSangkeetE_User.config = config
    KhunSangkeetE_User.parent_path = parent_path
    KhunSangkeetE_User.render_templates = FunctionForModule.render_templates
    KhunSangkeetE_User.genToken = FunctionForModule.gen_AdminToken_and_ItemId
    KhunSangkeetE_User.redirect = FunctionForModule.redirect_url
    KhunSangkeetE_User.userSys()
    app = KhunSangkeetE_User.app

    class UnicornException(Exception):
        def __init__(self, name: str):
            self.name = name

    @app.get("/favicon.ico")
    def icon():
        return "https://media.discordapp.net/attachments/1036704934432886876/1037321689073188894/cropped-it-logo.png"

    uvicorn.run(app, host=config["host"], port=int(config["port"]))
else:
     print("\x1b[31m Require File Error \x1b[0m")

