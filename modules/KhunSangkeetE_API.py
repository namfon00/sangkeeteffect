from fastapi.responses import JSONResponse, Response
import pandas as pd
import json

app = None
config = None
parent_path = None

def APISys():
    @app.get("/api")
    async def response_api(keyword=""):
        try:
            result = dict()
            if config["local_storage"]["on"] == 1:
                soundData = json.loads(open(parent_path+config["local_storage"]["sound data"], "r", encoding="utf-8").read())
                if keyword != "":
                    for _id in soundData:
                        if (not keyword.upper() in soundData[_id]["name"].upper())\
                        and (not keyword.upper() in soundData[_id]["description"].upper()):
                            result[_id] = soundData[_id]
                return JSONResponse(soundData, status_code=200)
            soundData = pd.read_csv(config["with_gform_and_gsheet"]["csv_link"])
            soundData = soundData.to_dict("index")
            if keyword != "":
                for _id in soundData:
                    if (not keyword.upper() in soundData[_id]["Sound Name"])\
                    and (not keyword.upper() in soundData[_id]["Description"]):
                        result[_id] = soundData[_id]
            return JSONResponse(result, status_code=200)
        except:
            return Response("404 Not Found", status_code=404)
