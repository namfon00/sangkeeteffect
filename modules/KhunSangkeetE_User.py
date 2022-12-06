from fastapi import  Form, Cookie, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
import pandas as pd
import json

app = None
config = None
parent_path = None
render_templates = None
redirect = None
genToken = None

def userSys():
    global app
    @app.get("/")
    async def home():
        """หน้าแรกของเว็บ"""
        #ให้ Pyton เอา ข้อมูลเสียง(.json) และ ไฟล์เสียงมาแสดง
        # ทำอันนี้
        soundData = json.loads(open(parent_path+config["local_storage"]["sound data"], "r").read())
        audioTag = ""
        for _id in soundData:
            audioTag += f"<audio controls src='/stream/sound/{_id}'></audio>"
        return HTMLResponse(render_templates(path=parent_path+"/templates/"+config["template"]["home"], data={"text":audioTag}))

    @app.get("/add_sound")
    async def add_sound():
        # แสดง หน้าเว็บสำหรับเพิ่มไฟล์
        if config["local_storage"]["on"] == 1:
            return HTMLResponse(render_templates(path=parent_path+"/templates/"+config["template"]["add_sound"], data={"id":genToken("id")}))
        return HTMLResponse(redirect(config["with_gform_and_gsheet"]["form_link"]))
    @app.post("/add_sound")
    async def save_sent_add_sound(
        _id = Form(""),
        soundName = Form(""),
        soundFile:UploadFile | None = None,
        description = Form("")
        ):
        if config["local_storage"]["on"] == 0:
            return HTMLResponse(redirect(config["with_gform_and_gsheet"]["form_link"]))
        try:
            soundData = json.loads(open(parent_path+config["local_storage"]["sound data"], "r").read())
        except:
            soundData = dict()
        soundData_W = open(parent_path+config["local_storage"]["sound data"], "w")
        soundData[_id]={
                "name":soundName,
                "description":description
            }
        soundData_W.write(json.dumps(soundData))
        soundData_W.close()
        file1 = open(f"{parent_path}{config['local_storage']['sound path']}/{_id}.mp3", "xb")
        file1.write(soundFile.file.read())
        file1.close()
        return HTMLResponse(redirect("/"))

    @app.get("/search")
    async def search(keyword: str = ""):
        """หน้าสำหรับแสดงผลค้นหา"""
        return HTMLResponse(render_templates(path=parent_path+"/templates/"+config["template"]["home"], data={"text":"Hello"}))

    @app.get("/info/{id}")
    async def show_info_sound(id:str = ""):
        """หน้าแสดงข้อมูลเสียง"""
        #แสดงข้อฒุลเสียง
        return HTMLResponse(render_templates(path = parent_path+"/templates/"+config["template"]["info"]))

    @app.get("/stream/sound/{id}")
    async def stream_sound(id: str = ""):
        """สตรีมไฟล์เสียง"""
        # Use in both admin and user
        if config["local_storage"]["on"] == 1:
            try:
                open(parent_path+config["local_storage"]["sound path"]+"/"+id+".mp3", "r")
                return FileResponse(parent_path+config["local_storage"]["sound path"]+"/"+id+".mp3")
            except:
                return HTMLResponse("Something Went Wrong Plase Check Path Or File Are Exist")
        return HTMLResponse(redirect("/"))

    @app.exception_handler(404)
    async def handler_error(req, exc):
        """แสดงหน้า 404 Error"""
        # Use in both admin and user
        return HTMLResponse(render_templates(path=parent_path+"/templates/"+config["template"]["err404"]))
