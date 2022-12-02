from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse, Response, PlainTextResponse
from pyngrok import ngrok as ngrokModule
import json
import os

app = None
config = None
cur_path_of_py_file = None
adminTemPath = None
admin_redirect = None
ngrok = None
ngrokLink = ""
parent_path = None
radminToken = ""
render_templates = None

def adminSys():
    global app
    def setNgrok():
        global ngrokLink
        if bool(config["ngrok"]["on"]) and config["ngrok"]["token"] != "" and ngrokLink == "":
            ngrokModule.set_auth_token(config["ngrok"]["token"])
            ngrokLink = "<tr><th>%s</th></tr>" % ngrokModule.connect(
                config["port"])
            print(ngrokLink)
        elif not bool(config["ngrok"]["on"]):
            ngrokLink = ""
            ngrokModule.kill()
    setNgrok()

    @app.get("/admin")
    def admin(adminToken: str = Cookie(None), err: str = ""):
        """
        หน้าแรกส่วนการตั้งค่า
        + Input
            + adminToken
            + err (เมื่อโทเค็นผิด)
        + Output
            + หน้า Login
            + หน้า Wellcome
            + Cookie (For Token)
        """
        admin_html = open(adminTemPath, "r").read()
        index_html = open(cur_path_of_py_file +
                        "/admin_templates/admin-login.txt", "r").read()
        if adminToken == radminToken:
            wellcome_html = open(cur_path_of_py_file +
                                "/admin_templates/admin-wellcome.txt", "r").read()
            if ngrokLink != "":
                wellcome_html = render_templates(wellcome_html, {"ngrokLinkBox": render_templates(open(cur_path_of_py_file+"/admin_templates/admin-wellcome-showNgrokLink.txt",
                                                                                                    "r").read(), {"ngrokLink": ngrokLink})})
            else:
                wellcome_html = render_templates(
                    wellcome_html, {"ngrokLinkBox": ""})
            return HTMLResponse(render_templates(admin_html, {"content": wellcome_html}))
        if err != "":
            index_html = render_templates(index_html, {"err": open(
                cur_path_of_py_file+"/admin_templates/admin-login-wrongToken.txt", "r").read()})
        else:
            index_html = render_templates(index_html, {"err": ""})
        return HTMLResponse(render_templates(admin_html, {"content": index_html}))


    @app.post("/admin")
    def admin_login(adminToken: str = Form("")):
        """
        ตรวจความถูกต้องของโทเค็น
        + Input
            + adminToken
        + Output
            + Cookie (เมื่อTokenผิด)
        """
        if adminToken == radminToken:
            response = HTMLResponse(admin_redirect)
            response.set_cookie(key="adminToken", value=adminToken)
            return response
        response = HTMLResponse("""
            <script>
                window.location.href = "/admin?err=Wrong Token"
            </script>
            """)
        response.delete_cookie(key="adminToken")
        return response


    @app.get("/admin/logout")
    def logout():
        """
        ออกจากระบบ
        + ทำการลบ Cookie
        """
        response = HTMLResponse(admin_redirect)
        response.delete_cookie(key="adminToken")
        return response


    @app.get("/admin/config")
    def config_html(adminToken=Cookie("")):
        """
        หน้าการกำหนดค่า
        + Input
            + adminToken
        """
        if adminToken != radminToken:
            return HTMLResponse(admin_redirect)
        admin_html = open(adminTemPath, "r").read()
        index_html = open(cur_path_of_py_file +
                        "/admin_templates/admin-config.txt", "r").read()
        data_cf = {
            "port": config["port"],
            "path": config["parent path"],
            "home": config["template"]["home"],
            "soundData": config["local_storage"]["sound data"],
            "soundStorage": config["local_storage"]["sound path"],
            "coverStorage": config["local_storage"]["cover path"],
            "withGsheetCheck": "checked" if config["with_gform_and_gsheet"]["on"] else "",
            "gFormLink": config["with_gform_and_gsheet"]["form_link"],
            "sheetLink": config["with_gform_and_gsheet"]["sheet_link"],
            "sheetLinkCSV": config["with_gform_and_gsheet"]["csv_link"],
            "ngrokDes": "สำหรับแชร์ Localhost",
            "ngrokLink": ngrokLink,
            "ngrokCheck": "checked" if config["ngrok"]["on"] else "",
            "ngrokToken": config["ngrok"]["token"]
        }
        index_html = render_templates(
            admin_html, {"content": render_templates(index_html, data_cf)})
        return HTMLResponse(index_html)


    @app.post("/admin/config")
    def set_config(
            adminToken=Cookie(""),
            port: str = Form(config["port"]),
            path: str = Form(""),
            home: str = Form(""),
            storageType: str = Form(""), sheetLink: str = Form(""), sheetLinkCSV: str = Form(""),
            gFormLink: str = Form(""),
            ngrok: bool = Form(""), ngrokToken: str = Form("")):
        """
        บันทึกค่าการตั้งค่าลงไฟล์ เจสัน
        + Input
            + adminToken
            + port (fix)
            + path
            + (path .... page)
                + home 
            + storageType
                + sheetLink
                + sheetLinkCSV
                + gFormLink
            + ngrok
                + ngrokToken
        """
        if adminToken != radminToken:
            return HTMLResponse(admin_redirect)
        global config, ngrokLink
        # config หลัก
        config_js = open(cur_path_of_py_file+"/data/config.json", "w")
        config["port"] = port
        config["parent path"] = path
        config["template"]["home"] = home
        # config ประเภทที่เก็บข้อมูล และ ที่อยู่ของข้อมูล
        if storageType == "local":
            config["with_gform_and_gsheet"]["on"] = 0
            config["local_storage"]["on"] = 1
        else:
            config["with_gform_and_gsheet"]["on"] = 1
            config["local_storage"]["on"] = 0
        config["with_gform_and_gsheet"]["form_link"] = gFormLink
        config["with_gform_and_gsheet"]["sheet_link"] = sheetLink
        config["with_gform_and_gsheet"]["csv_link"] = sheetLinkCSV
        # config ngrok
        if ngrok:
            config["ngrok"]["on"] = 1
            config["ngrok"]["token"] = ngrokToken
            setNgrok()
        else:
            config["ngrok"]["on"] = 0
            config["ngrok"]["token"] = ngrokToken
            setNgrok()
        config_js.write(json.dumps(config))
        config_js.close()
        return HTMLResponse("""
        <script>
            window.location.href = "./config"
        </script>
        """)


    @app.get("/admin/edit")
    def showFileCanEdit(adminToken=Cookie(""), filepath: str = ""):
        """
        หน้าแก้ไขไฟล์
        + Input
            + adminToken
            + ?filepath
        + Output
            + รายการไฟล์ต่างๆ
        """
        admin_html = open(adminTemPath, "r").read()
        if adminToken != radminToken:
            return HTMLResponse(admin_redirect)
        if filepath != "":
            if "admin-" in filepath:
                return HTMLResponse(render_templates(admin_html, {"content":"Admin File Can't Edit Here"}))
            return HTMLResponse(render_templates(admin_html, {"content":
            render_templates(open(cur_path_of_py_file+"/admin_templates/admin-edit-textarea.txt", "r").read()
                , { "filePath":filepath,
                    "textFile":open(parent_path+"/"+filepath, "r").read()
                    })})
            )
        ct = ""
        for file_name in os.listdir(parent_path+"/templates"):
            ct += f"""<tr><td>{'''
            <span class="material-symbols-outlined">lock</span>''' if "admin-" in file_name else 
            '''<span class="material-symbols-outlined">draft</span>'''}
            <a href='?filepath={"templates/"+file_name}'>{file_name}</a>
            </td></tr>\n"""
        ct = render_templates(open(cur_path_of_py_file+"/admin_templates/admin-edit.txt", "r").read(),
                            {"templateFiles": ct})
        if config["with_gform_and_gsheet"]["on"]:
            ct = render_templates(ct, {"soundData": f"""
                <p>View Only (Edit at <a href="{config["with_gform_and_gsheet"]["sheet_link"]}">Link)</a></p>
                <iframe width="100%" height="100%" style="min-height: 500px;" src="{config["with_gform_and_gsheet"]["csv_link"][:config["with_gform_and_gsheet"]["csv_link"].find("&")]}" ></iframe>
            """})
        index_html = render_templates(
            admin_html, {"content": ct if filepath == "" else filepath})
        return HTMLResponse(index_html)

    @app.post("/admin/edit")
    def save_file_from_admin_edit(textFile:str=Form(""), pathFile=Form("")):
        """
        บันทึกไฟล์ จากหน้าEdit
        + Input
            + textFile
            + pathFile
        + Output
            + ไฟล์ / ข้อมูล ท่ีบันทึกแล้ว
        """
        file_ = open(parent_path+"/"+pathFile, "w")
        file_.write(textFile)
        file_.close()
        return "Success"
