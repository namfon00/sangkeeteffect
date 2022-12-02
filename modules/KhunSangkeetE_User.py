from fastapi import FastAPI, Request, Form, Cookie, File
from fastapi.responses import HTMLResponse, StreamingResponse, Response, FileResponse
from pyngrok import ngrok as ngrokModule
import pandas as pd
import uvicorn
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
    def home():
        """หน้าแรกของเว็บ"""
        return HTMLResponse(render_templates(path=parent_path+config["template"]["home"], data={"text":"Hello"}))

    @app.get("/add_sound")
    def add_sound():
        return HTMLResponse(genToken("id"))

    @app.post("/add_sound")
    def save_sent_add_sound():
        
        return HTMLResponse(redirect("/add_sound"))

    @app.get("/search")
    def search(keyword: str = ""):
        """หน้าสำหรับแสดงผลค้นหา"""
        return HTMLResponse(render_templates(path=parent_path+config["template"]["home"], data={"text":"Hello"}))

    @app.get("/info/{id}")
    def show_info_sound(id:str = ""):
        """หน้าแสดงข้อมูลเสียง"""
        return HTMLResponse(render_templates(path = parent_path+config["template"]["info"]))

    @app.get("/stream/sound/{id}")
    def stream_sound(id: str = ""):
        """สตรีมไฟล์เสียง"""
        # Use in both admin and user
        if config["local_storage"]["on"] == 0:
            return HTMLResponse(redirect("/"))
        return FileResponse(parent_path+config["local_storage"]["sound path"]+"/"+id+".mp3")

    @app.exception_handler(404)
    def handler_error(req, exc):
        # Use in both admin and user
        return HTMLResponse(render_templates(path=parent_path+config["template"]["err404"]))
