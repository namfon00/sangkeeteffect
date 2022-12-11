"""ป้องกันการErrorเมื่อไฟล์ Admin/config หาย!!!
ไฟล์ที่จำเป็น
+ config.json #important!!!
+ admin-tem.txt
+ admin-login.txt
+ admin-login-wrongToken.txt
+ admin-wellcome.txt
+ admin-wellcome-showNgrokLink.txt
+ admin-config.txt
+ admin-edit.txt
+ admin-edit-textarea.txt
"""
import os
import json
import time
import requests
import platform
import pandas as pd

def get_content_from_github(filename):
    return requests.get("https://raw.githubusercontent.com/namfon00/sangkeeteffect/main/admin_templates/"+filename).text

limit_option = False

list_req_folders = [
    '/admin_templates',
    '/data'
]
list_req_file_in_data = [
    'config.json'
    ]
list_req_file_in_adminTemplate = [
    'admin-edit-dataSoundRow.txt', 
    'admin-tem.txt', 
    'admin-edit-dataSound.txt', 
    'admin-edit-textarea.txt', 
    'admin-welcome-showNgrokLink.txt', 
    'admin-edit.txt',
    'admin-edit-editSoundData.txt', 
    'admin-config.txt', 
    'admin-login.txt', 
    'admin-welcome.txt', 
    'admin-login-wrongToken.txt'
    ]
req_file_content = {
    'config.json':json.dumps({"host": "localhost", "port": "8080", "parent path": "./", "template": {"home": "home.html", "add_sound": "add_sound.html", "info": "info.html", "err404": "404.html"}, "ngrok": {"on": 0, "token": ""}, "local_storage": {"on": 1, "sound data": "/data/sound_data.json", "sound path": "/data/sound"}, "with_gform_and_gsheet": {"on": 0, "form_link": "https://forms.gle/TCcyW8BmLQJmcbtC8", "sheet_link": "https://docs.google.com/spreadsheets/d/1OU-fN7NAYX68PAAeAm-W3ppEa3eFSE0dtsL-Glxn0ZI/edit", "csv_link": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTcV3Nob9Hk2j2eKRQpP3IaYZ1UFCPVQ9YGdmnAzl5TorIi7DhDcA5e7EJWQCI_8nXkuuqx5l5YdBwY/pub?gid=203295964&single=true&output=csv"}, "send_token_to_discord": {"on": 1, "webhook_url": "https://discord.com/api/webhooks/1045772264399962125/cueDxMti8ihX2HtKuUrWYXRsVMgU_stHBtvQz-3wPND8J9M7aB2DNIt6Wko9EmWe6BGq", "show_os": 1, "show_ip": 1}}), 
    'sound_data.json': json.dumps({}),
    'admin-tem.txt': "#from_internet",#get_content_from_github("admin-tem.txt"), 
    'admin-login.txt': "#from_internet",#get_content_from_github("admin-login.txt"),
    'admin-login-wrongToken.txt': "#from_internet",#get_content_from_github("admin-login-wrongToken.txt"),
    'admin-welcome.txt': "#from_internet",#get_content_from_github("admin-welcome.txt"),
    'admin-welcome-showNgrokLink.txt': "#from_internet",#get_content_from_github("admin-welcome-showNgrokLink.txt"), 
    'admin-config.txt': "#from_internet",#get_content_from_github("admin-config.txt"),
    'admin-edit.txt': "#from_internet",#get_content_from_github("admin-edit.txt"),
    'admin-edit-textarea.txt': "#from_internet",#get_content_from_github("admin-edit-textarea.txt"),
    'admin-edit-dataSound.txt': "#from_internet",#get_content_from_github("admin-edit-dataSound.txt"), 
    'admin-edit-dataSoundRow.txt': "#from_internet",#get_content_from_github("admin-edit-dataSoundRow.txt"), 
    'admin-edit-editSoundData.txt': "#from_internet",#get_content_from_github("admin-edit-editSoundData.txt"),
}
check_list = []
gb_want_to_fix = False
def checkSys():
    global limit_option
    print("\x1b[30;48;5;250m=======================   Checking Python Version And SSL Cert    =======================\x1b[0m")
    if int(platform.python_version()[:platform.python_version().find(".")]) == 3\
    and int(platform.python_version()[platform.python_version().find(".")+1:platform.python_version().find(".",3)]) >= 10:
        print("\x1b[1;38;5;114m Checked : \x1b[0mYour Python vesion "+platform.python_version())
    else:
        print("\x1b[1;38;5;160m Python Must Be 3.10 Or Above Not : \x1b[0mYour Python vesion "+platform.python_version())
        return False
    import ssl
    print("\x1b[1;38;5;114m Checked : \x1b[0m"+platform.system())
    if platform.system() != "Darwin":
        pass
    elif  ssl.get_default_verify_paths().capath != None or \
        ssl.get_default_verify_paths().cafile != None:
        cert_path = ssl.get_default_verify_paths().cafile if ssl.get_default_verify_paths().cafile!=None else ssl.get_default_verify_paths().capath
        print("\x1b[1;38;5;114m Checked : \x1b[0m SSL Certificate"+cert_path)
    else:
        print("\x1b[1;38;5;160m SSL Certificate Not Available : \x1b[0mLimit Option Can Used In App")
        limit_option = True
    req_path = __file__[:__file__.rfind("/") if __file__.rfind("/") != -1 else __file__.rfind("\\")]
    req_path = req_path[:req_path.rfind("/") if req_path.rfind("/") != -1 else req_path.rfind("\\")]
    def askForFix(path, _type, force_fix):
        global check_list, gb_want_to_fix
        if not gb_want_to_fix:
            print("\x1b[38;5;220m Want To Fix It [Y]es/[N]o/[A]ll?\x1b[0m")
            want_to_fix = input(">> ")
        if gb_want_to_fix or want_to_fix.upper() == "A" or want_to_fix.upper() == "ALL":
            gb_want_to_fix = True
        if gb_want_to_fix or want_to_fix.upper() == "Y" or want_to_fix.upper() == "YES":
            if _type == "folder":
                os.mkdir(path)
            elif _type == "file":
                file_name = path[path.rfind("/")+1 if path.rfind("/") != -1 else path.rfind("\\")+1:]
                if not file_name in req_file_content:
                    print(f"\x1b[38;5;220m Auto Fix Can't Fix {path} Plase Fix By Yourself.\x1b[0m")
                    return 0
                file_w = open(path, "x", encoding="utf-8")
                req_file_content_key = file_name if force_fix == "" else force_fix
                req_file_content[req_file_content_key] = req_file_content[req_file_content_key] if req_file_content[req_file_content_key] != "#from_internet" else get_content_from_github(req_file_content_key)
                file_w.write(req_file_content[req_file_content_key])
                file_w.close()
            print("\x1b[1;38;5;114m Fixed : \x1b[0m"+path)
            check_list[-1] = True
    def checkFileOrFolderAreExist(path, _type, force_fix=""):
        global check_list
        time.sleep(0.15)
        try:
            if _type == "folder":
                os.listdir(path)
            elif _type == "file":
                ctf = open(path, "r", encoding="utf-8").read()
        except:
            print("\x1b[1;38;5;160m Not Found : \x1b[0m"+path)
            check_list.append(False)
            askForFix(path=path, _type=_type, force_fix=force_fix)
        else:
            if _type == "file" and ctf == "":
                check_list.append(False)
                print("\x1b[1;38;5;160m No Content In File : \x1b[0m"+path)
                askForFix(path=path, _type=_type, force_fix=force_fix)
            else:
                check_list.append(True)
                print("\x1b[1;38;5;114m Checked : \x1b[0m"+path)

    print("\x1b[30;48;5;250m=========================   Checking Require File And Folder    =========================\x1b[0m")
    for folder in list_req_folders:
        checkFileOrFolderAreExist(req_path+folder, _type="folder")
    for file in list_req_file_in_data:
        checkFileOrFolderAreExist(f"{req_path}/data/{file}", _type="file")
    for file in list_req_file_in_adminTemplate:
        checkFileOrFolderAreExist(f"{req_path}/admin_templates/{file}", _type="file")
    print("\x1b[30;48;5;250m=================   Checking Path File And Folder In Config Are Exits   ================\x1b[0m")
    try:
        config = json.loads(open(f"{req_path}/data/config.json", "r", encoding="utf-8").read())
    except:
        print("\x1b[1;38;5;160m Error : No Config File !!\x1b[0m")
        return False
    else:
        config["parent path"] = config["parent path"] if config["parent path"] != "./" else req_path
        checkFileOrFolderAreExist(config["parent path"], _type="folder")
        checkFileOrFolderAreExist(config["parent path"]+"/templates", _type="folder")
        for file_name in config["template"]:
            checkFileOrFolderAreExist(f'{config["parent path"]}/templates/{config["template"][file_name]}', _type="file")
        checkFileOrFolderAreExist(config["parent path"]+"/data", _type="folder")
        checkFileOrFolderAreExist(f'{config["parent path"]}{config["local_storage"]["sound data"]}', _type="file", force_fix="sound_data.json")
        checkFileOrFolderAreExist(f'{config["parent path"]}{config["local_storage"]["sound path"]}', _type="folder")
    print("\x1b[30;48;5;250m=================================      End Checking     =================================\x1b[0m")
    return all(check_list)
