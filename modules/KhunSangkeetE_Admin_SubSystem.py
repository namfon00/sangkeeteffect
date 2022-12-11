from fastapi import Cookie
from fastapi.responses import HTMLResponse
import requests
import os

app = None
config = {}
render_templates = None
redirect = None
cur_path_of_py_file = ""
parent_path = None
adminTemPath = ""
alert = None
alert_mss = ""
radminToken = ""
admin_redirect = None

def adminSubSys():
    def render_adminTemplates(content:str = ""):
        global alert_mss
        _alert = f"<script>{alert(mss = alert_mss)}</script>" if alert_mss != "" else ""
        result_html = render_templates(path = adminTemPath, data = {"content":content,"alert":_alert})
        alert_mss = ""
        return result_html
    def checkForAdminCheck(topic):
        result = ""
        if topic == "home"\
        or topic == "add_sound"\
        or topic == "info"\
        or topic == "err404":
            try:
                f = open(parent_path+"/templates/"+config["template"][topic], "r", encoding="utf-8").read()
                if f.strip() == "":
                    result += "<font class='warning'>Warning This File Is Blank : </font>/templates/"+config["template"][topic]
                    del f
                else:
                    result += "<font class='success'>No Problem With : </font>/templates/"+config["template"][topic]
            except:
                result += "<font class='danger'>Error File Not Exist : </font>/templates/"+config["template"][topic]
        if topic == "sound data":
            try:
                f = open(parent_path+config["local_storage"][topic], "r", encoding="utf-8").read()
                if f.strip() == "":
                    result += "<font class='warning'>Warning This File Is Blank : </font>"+config["local_storage"][topic]
                    del f
                else:
                    result += "<font class='success'>No Problem With : </font>"+config["local_storage"][topic]
            except:
                result += "<font class='danger'>Error File Not Exist : </font>"+config["local_storage"][topic]
        elif topic == "sound path":
            try:
                os.listdir(parent_path+config["local_storage"][topic])
                result += "<font class='success'>No Problem With : </font>"+config["local_storage"][topic]
            except:
                result += "<font class='danger'>Error Directory Not Exist : </font>"+config["local_storage"][topic]
        if topic == "form_link"\
        or topic == "sheet_link"\
        or topic == "csv_link":
            req = requests.get(config["with_gform_and_gsheet"][topic])
            if req.status_code//100 == 2:
                result += f"<font class='success'>No Problem {topic} Requests Status Code : </font>{req.status_code}"
            else:
                result += f"<font class='danger'>Requests Error Status Code : </font>{req.status_code}"
        if topic == "all_template" or topic == "all":
            result += checkForAdminCheck("home")+"<br/>"
            result += checkForAdminCheck("add_sound")+"<br/>"
            result += checkForAdminCheck("info")+"<br/>"
            result += checkForAdminCheck("err404")+"<br/>"
        if topic == "all_local_storage" or topic == "all":
            result += checkForAdminCheck("sound data")+"<br/>"
            result += checkForAdminCheck("sound path")+"<br/>"
        if topic == "all_with_gform_and_gsheet" or topic == "all":
            result += checkForAdminCheck("form_link")+"<br/>"
            result += checkForAdminCheck("sheet_link")+"<br/>"
            result += checkForAdminCheck("csv_link")+"<br/>"
        return result
    @app.get("/admin/check")
    def checkError(topic="", adminToken=Cookie("")):
        if adminToken != radminToken:
            return HTMLResponse(admin_redirect)
        result = ""
        if topic.strip() != "":
            result = checkForAdminCheck(topic)
        return HTMLResponse(render_adminTemplates(
            render_templates(
                path = cur_path_of_py_file+"/admin_templates/admin-checkError.txt",
                data = {
                    "result":"<section class='form-control result'><h1>Result</h1>No Result Now</section>" if result == "" else f"<section class='form-control result'><h1>Result</h1>{result}</section>"
                }
                )
        ))
