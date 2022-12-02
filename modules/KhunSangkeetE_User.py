from fastapi import FastAPI, Request, Form, Cookie
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

def userSys():
    global app
    @app.get("/")
    def home():
        """หน้าแรกของเว็บ"""
        index_html = open(parent_path+config["template"]["home"], "r", encoding="utf-8").read()
        return HTMLResponse(index_html.replace("/*text*/", "Hello"))


    @app.get("/search")
    def search(keyword: str):
        """หน้าสำหรับแสดงผลค้นหา"""
        index_html = open(parent_path+config["template"]["home"], "r", encoding="utf-8").read()
        return HTMLResponse(index_html.replace("/*text*/", keyword))

    @app.get("/info")
    def show_info_sound():
        return "Inprogress"

    @app.get("/stream/sound/{id}")
    def stream_sound(id: str = ""):
        # Use in both admin and user
        return FileResponse(parent_path+config["local_storage"]["sound path"]+"/"+id+".mp3")

