import requests
import platform
import secrets

cur_path_of_py_file = None
config = {}
def gen_AdminToken_and_ItemId(_type:str = "token"):
    """Generate Token for Login and Generate Id for Item
    สร้างTokenในการใช้Login และสร้าง Id สำหรับข้อมูล"""
    adminToken = secrets.token_urlsafe(20)
    if _type == "token":
        adminToken = secrets.token_urlsafe(30)
        print("\x1b[36mToken : "+adminToken+"\x1b[0m")
        send_to_discord(token=adminToken)
    return adminToken
def render_templates(index_html:str = "", data:dict = {}, path:str = ""):
    """Render templates
        Usage วิธีใช้
        /*name*/ in html for point position where should replace by value
        วาง /*n...*/ เพื่อรระบุตำแหน่งที่ะแทนค่า
        (index_html:str, data:dict, [path:str])
        sample
            render_templates("<h1>/*head1*/</h1>",{"head1":"Hello"})
            result : <h1>Hello</h1>
    """
    #ใช้ทดแทน Module templating ของ Fastapi ที่เกิดปัญหากับภาษาไทย
    try:
        if path != "":
            index_html = open(path, "r", encoding="utf-8").read()
        for i in data:
            index_html = index_html.replace(f"/*{i}*/", str(data[i]))
    except:
        index_html = "Something Went Wrong Plase Check Path In Config Or Check Which Files Are Lose. <a href='/admin/check'>Check Here</a>"
    return index_html
def redirect_url(url_path = "/"):
    """redirect_url"""
    #ใช้ทดแทน Module RedirectResponse ของ Fastapi ที่เกิดปัญหา เปลี่ยนเส้นทางของคุณบ่อยเกินไป(ERR_TOO_MANY_REDIRECTS)
    return f"""<script> window.location.href = "{url_path}" </script>"""
def alert(icon:str = "info" ,mss:str = ""):
    if "wrong" in mss.lower() or "error" in mss.lower():
        icon = "error"
    elif "success" in mss.lower():
        icon = "success"
    if mss == "" or mss == None:
        return ""
    result = """ 
            Toast.fire({
                icon: '%s',
                title: '%s',
                color: '%s'
                });
            """%(icon, mss, "var(--bs-danger)" if icon == "error" else "var(--bs-success)" if icon == "success" else "")
    return result
def send_to_discord(token="", ngrok_link=""):
    if  not config["send_token_to_discord"]["on"]:
        return ""
    if config["send_token_to_discord"]["webhook_url"] != "":
        requests.post(config["send_token_to_discord"]["webhook_url"],
        json={
                "content": "",
                "embeds": [
                    {
                    "title": "Your TokenKey" if token != "" else "Ngrok Link",
                    "description": "%s "% "Token : " + token if token != "" else "Link : "+ngrok_link,
                    "color": 7559423 if token != "" else 5199043,
                    "footer":{
                        "text": "%s %s"
                        %("Running From : " + platform.platform() if config["send_token_to_discord"]["show_os"] == 1 else " ",
                        "| Ip : "+str(requests.get("https://api.ipify.org").content, encoding="utf-8") if config["send_token_to_discord"]["show_ip"] == 1 else "")
                    }
                    }
                ],
                "username": "KhunSangkeet E-Admin",
                "attachments": []
            })
