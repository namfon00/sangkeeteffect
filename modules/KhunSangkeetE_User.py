from fastapi import  Form, UploadFile, Cookie
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
        try:
            soundDataHTML = ""
            if config["local_storage"]["on"] == 1:
                soundData = json.loads(open(parent_path+config["local_storage"]["sound data"], "r").read())
                for _id in soundData.keys():
                    soundDataHTML += f"""<div class="card" id="{_id}" onclick="togglePlay('{_id}','/stream/sound/{_id}')">
                                <center>
                                <span class="material-symbols-outlined" style="font-size: 100px;font-weight: 1500; color: grey">
                                music_note
                                </span>
                                <p>{soundData[_id]["name"]}<a href="/info/{_id}"><span class="material-symbols-outlined">
                                info
                                </span>
                                </a>
                                </p>
                                </center>
                            </div>"""
                return HTMLResponse(render_templates(
                    path=parent_path+"/templates/"+config["template"]["home"], 
                    data={
                        "soundData":soundDataHTML
                        }))
            soundData = pd.read_csv(config["with_gform_and_gsheet"]["csv_link"])
            soundData = soundData.to_dict("index")
            #https://drive.google.com/uc?export=download&id=
            for _id in soundData.keys():
                    soundDataHTML += f"""<div class="card" id="{_id}" onclick="togglePlay('{_id}','https://drive.google.com/uc?export=download&id={soundData[_id]["Sound File"][soundData[_id]["Sound File"].find("?id=")+4:]}')">
                                <center>
                                <span class="material-symbols-outlined" style="font-size: 100px;font-weight: 1500; color: grey">
                                music_note
                                </span>
                                <p>{soundData[_id]["Sound Name"]}<a href="/info/{_id}"><span class="material-symbols-outlined">
                                info
                                </span>
                                </a>
                                </p>
                                </center>
                            </div>"""
            return HTMLResponse(render_templates(
                    path=parent_path+"/templates/"+config["template"]["home"], 
                    data={
                        "soundData":soundDataHTML
                        }))
        except:
            return HTMLResponse(render_templates(
                path=parent_path+"/templates/"+config["template"]["home"], 
                    data={
                        "soundData":"มีบางอย่างผิดพลาดโปรดติดต่อผู้ดูแล"
                        }))

    @app.get("/add_sound")
    async def add_sound():
        # แสดง หน้าเว็บสำหรับเพิ่มไฟล์
        if config["local_storage"]["on"] == 1:
            return HTMLResponse(render_templates(
                path=parent_path+"/templates/"+config["template"]["add_sound"], 
                data={
                    "id":genToken("id")
                    }))
        return HTMLResponse(redirect(config["with_gform_and_gsheet"]["form_link"]))
    @app.post("/add_sound")
    async def save_sent_add_sound(
        _id = Form(""),
        soundName = Form(""),
        soundFile:UploadFile | None = None,
        description = Form("")
        ):
        if config["local_storage"]["on"] == 1:
            try:
                soundData = json.loads(open(parent_path+config["local_storage"]["sound data"], "r", encoding="utf-8").read())
            except:
                soundData = dict()
            soundData_W = open(parent_path+config["local_storage"]["sound data"], "w", encoding="utf-8")
            soundData[_id]={
                    "name":soundName,
                    "description":description
                }
            soundData_W.write(json.dumps(soundData))
            soundData_W.close()
            file1 = open(f"{parent_path}{config['local_storage']['sound path']}/{_id}.mp3", "xb")
            file1.write(soundFile.file.read())
            file1.close()
            return HTMLResponse(redirect(f"/info/{_id}"))
        return HTMLResponse(redirect(config["with_gform_and_gsheet"]["form_link"]))

    @app.get("/search")
    async def search(keyword: str = ""):
        """หน้าสำหรับแสดงผลค้นหา"""
        try:
            soundDataHTML = ""
            if keyword == "":
                return HTMLResponse(redirect("/"))
            if config["local_storage"]["on"] == 1:
                soundData = json.loads(open(parent_path+config["local_storage"]["sound data"], "r", encoding="utf-8").read())
                for _id in soundData:
                    if keyword.upper() in soundData[_id]["name"].upper():
                        soundDataHTML += f"""<div class="card" id="{_id}" onclick="togglePlay('{_id}','/stream/sound/{_id}')">
                                <center>
                                <span class="material-symbols-outlined" style="font-size: 100px;font-weight: 1500; color: grey">
                                music_note
                                </span>
                                <p>{soundData[_id]["name"]}<a href="/info/{_id}"><span class="material-symbols-outlined">
                                info
                                </span>
                                </a>
                                </p>
                                </center>
                            </div>"""
                return HTMLResponse(render_templates(
                    path=parent_path+"/templates/"+config["template"]["home"], 
                    data={
                        "soundData":soundDataHTML if len(soundDataHTML) > 0 else "หาไม่พบ "+keyword,
                        }
                ))
            soundData = pd.read_csv(config["with_gform_and_gsheet"]["csv_link"])
            soundData = soundData.to_dict("index")
            # https://drive.google.com/uc?export=download&id=
            for _id in soundData:
                    if keyword.upper() in soundData[_id]["Sound Name"].upper():
                        soundDataHTML += f"""<div  class="card" id="{_id}" onclick="togglePlay('{_id}','https://drive.google.com/uc?export=download&id={soundData[_id]["Sound File"][soundData[_id]["Sound File"].find("?id=")+4:]}')">
                                <center>
                                <span class="material-symbols-outlined" style="font-size: 100px;font-weight: 1500; color: grey">
                                music_note
                                </span>
                                <p>{soundData[_id]["Sound Name"]}<a href="/info/{_id}"><span class="material-symbols-outlined">
                                info
                                </span>
                                </a>
                                </p>
                                </center>
                            </div>"""
            return HTMLResponse(render_templates(
                    path=parent_path+"/templates/"+config["template"]["home"], 
                    data={
                        "soundData":soundDataHTML if len(soundDataHTML) > 0 else "หาไม่พบ "+keyword
                        }))
        except:
            return HTMLResponse(redirect("/"))
    @app.get("/info/{_id}")
    async def show_info_sound(_id:str = ""):
        """หน้าแสดงข้อมูลเสียง"""
        #แสดงข้อฒุลเสียง
        try:
            if config["local_storage"]["on"] == 1:
                soundData = json.loads(open(parent_path+config["local_storage"]["sound data"], "r", encoding="utf-8").read())
                return HTMLResponse(render_templates(
                    path = parent_path+"/templates/"+config["template"]["info"],
                    data = {
                        "id":_id,
                        "soundName":soundData[_id]["name"],
                        "description":soundData[_id]["description"],
                        "link":"/stream/sound/"+_id
                    }
                    ))
            soundData = pd.read_csv(config["with_gform_and_gsheet"]["csv_link"])
            soundData = soundData.to_dict("index")
            return HTMLResponse(render_templates(
                path = parent_path+"/templates/"+config["template"]["info"],
                data = {
                    "id":_id,
                    "soundName":soundData[int(_id)]["Sound Name"],
                    "description":soundData[int(_id)]["Description"],
                    "link":"https://drive.google.com/uc?export=download&id="+soundData[int(_id)]["Sound File"].split("?id=")[1]
                
                }
                ))
        except:
            return HTMLResponse(redirect("/"))
        

    @app.get("/stream/sound/{_id}")
    async def stream_sound(_id: str = ""):
        """สตรีมไฟล์เสียง"""
        # Use in both
        if config["local_storage"]["on"] == 1:
            try:
                open(parent_path+config["local_storage"]["sound path"]+"/"+_id+".mp3", "r")
                return FileResponse(parent_path+config["local_storage"]["sound path"]+"/"+_id+".mp3")
            except:
                return HTMLResponse("มีบางผิดตกปิโปรดตรวจสอบว่าไฟล์มีอยู่หรือไม่!?")
        return HTMLResponse(redirect("/"))

    @app.exception_handler(404)
    async def handler_error(req, exc):
        """แสดงหน้า 404 Error"""
        # Use in both
        try:
            return HTMLResponse(render_templates(path=parent_path+"/templates/"+config["template"]["err404"]))
        except:
            return "404 File Not Found หาไฟล์ไม่เจออออออออออออออออออออออ"
