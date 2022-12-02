from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse, Response, PlainTextResponse
from pyngrok import ngrok as ngrokModule
import pandas as pd
import uvicorn
import json
import random
import os

app = None
config = None
parent_path = None
render_templates = None

def userSys():
    global app
    @app.get("/")
    def home():
        """หน้าแรกของเว็บ"""
        index_html = open(parent_path+config["template"]["home"], "r").read()
        return HTMLResponse(index_html.replace("/*text*/", "Hello"))


    @app.get("/search")
    def search(keyword: str):
        """หน้าสำหรับแสดงผลค้นหา"""
        index_html = open(parent_path+config["template"]["home"], "r").read()
        return HTMLResponse(index_html.replace("/*text*/", keyword))

    @app.get("/info")
    def show_info_sound():
        return "Inprogress"