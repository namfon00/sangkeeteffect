from fastapi import FastAPI, Request, Form, Cookie, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse, Response, FileResponse
from pyngrok import ngrok as ngrokModule
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
            audioTag += f"<audio control src='/stream/sound/{_id}'/>"
        return HTMLResponse(render_templates(path=parent_path+config["template"]["home"], data={"text":audioTag}))

    @app.get("/add_sound")
    async def add_sound():
        # แสดง หน้าเว็บสำหรับเพิ่มไฟล์
        if config["local_storage"]["on"] == 1:
            return HTMLResponse(render_templates(path=parent_path+config["template"]["add_sound"], data={"id":genToken("id")}))
        return HTMLResponse(redirect(config["with_gform_and_gsheet"]["form_link"]))
    @app.post("/add_sound")
    async def save_sent_add_sound(
        _id = Form(""),
        soundName = Form(""),
        soundFile:UploadFile = UploadFile,
        description = Form("")
        ):
        #บันทึกไฟล์จาการอัปโหลด // ไปดูตัวอย่างที่ sample_upload.py
        #open(parent_path+config["local_storage"][""])
        a = soundFile.file.read()
        fil = open(parent_path+""+_id+".mp3","wb")
        fil.write(a)
        fil.close()
        return {1:soundFile,soundFile.filename:_id}

    @app.get("/search")
    async def search(keyword: str = ""):
        """หน้าสำหรับแสดงผลค้นหา"""
        return HTMLResponse(render_templates(path=parent_path+config["template"]["home"], data={"text":"Hello"}))

    @app.get("/info/{id}")
    async def show_info_sound(id:str = ""):
        """หน้าแสดงข้อมูลเสียง"""
        #แสดงข้อฒุลเสียง
        return HTMLResponse(render_templates(path = parent_path+config["template"]["info"]))

    @app.get("/stream/sound/{id}")
    async def stream_sound(id: str = ""):
        """สตรีมไฟล์เสียง"""
        # Use in both admin and user
        if config["local_storage"]["on"] == 1:
            return FileResponse(parent_path+config["local_storage"]["sound path"]+"/"+id+".mp3")
        return HTMLResponse(redirect("/"))

    @app.exception_handler(404)
    async def handler_error(req, exc):
        """แสดงหน้า 404 Error"""
        # Use in both admin and user
        return HTMLResponse(render_templates(path=parent_path+config["template"]["err404"]))
