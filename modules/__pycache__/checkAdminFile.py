"""ป้องกันการErrorเมื่อไฟล์ Admin/config หาย!!!
ไฟล์ที่จำเป็น
+ config.json #important!!!
+ admin-tem.txt
+ admin-login.txt
+ admin-login-wrongToken.txt
+ admin-wellcome.txt
+ admin-wellcome-showNgrokLink.txt
+ admin-config.txt
+ admin-edit.txt
+ admin-edit-textarea.txt
"""
list_req_admin_file = [
    "config.json",
    "admin-tem.txt",
    "admin-login.txt",
    "admin-login-wrongToken.txt",
    "admin-wellcome.txt",
    "admin-wellcome-showNgrokLink.txt",
    "admin-config.txt",
    "admin-edit.txt",
    "admin-edit-textarea.txt"
    ]

config_data = """{"host": "localhost", "port": "8080", "parent path": "./", "template": {"home": "/templates/home.txt"}, "ngrok": {"on": 0, "token": "2E9lFpayxjyEXqPEl1fCCiibujh_7S1itcMv8pfBofs5L3iWG"}, "local_storage": {"on": 0, "sound data": "/data/sound_data.json", "sound path": "/sound", "cover path": "/cover"}, "with_gform_and_gsheet": {"on": 1, "form_link": "https://forms.gle/TCcyW8BmLQJmcbtC8", "sheet_link": "https://docs.google.com/spreadsheets/d/1OU-fN7NAYX68PAAeAm-W3ppEa3eFSE0dtsL-Glxn0ZI/edit", "csv_link": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTcV3Nob9Hk2j2eKRQpP3IaYZ1UFCPVQ9YGdmnAzl5TorIi7DhDcA5e7EJWQCI_8nXkuuqx5l5YdBwY/pub?gid=1384870553&single=true&output=csv"}}"""

admin_tem = """<!DOCTYPE html>
<html lang="en"> <head> <meta charset="UTF-8"/> <meta http-equiv="X-UA-Compatible" content="IE=edge"/> <meta name="viewport" content="width=device-width, initial-scale=1.0"/> <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous"/> <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"/> <style>@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai&display=swap'); *{font-family: 'Noto Sans Thai', sans-serif;}body{overflow: hidden; height: 100vh;}span{display:inline-block; vertical-align: text-top;}h1>span.material-symbols-outlined, h2>span.material-symbols-outlined, h4>span.material-symbols-outlined{font-size:2.5rem;}.big-content{display: flex; width: 100%; height: 100%;}.big-content>nav{padding: 20px; min-width: fit-content; width: 25vw; border-right: solid 1px var(--bs-gray-300);}.navbar{padding: 10px; border-bottom: solid 1px var(--bs-gray-300);}.ct-form{overflow-y: scroll; width: 100%; padding: 20px; max-height: 100%;}.ct-form>div{min-height:fit-content; margin-bottom:50vh;}table{width: 100%;}tr, td{vertical-align: top; padding: 10px;}.list-admin-content, .nav-bar-content{color : var(--bs-gray-800); text-decoration : none;}.list-admin-content{display:block; padding-top:15px;}.ct-edit{height:fit-content; max-height: 600px; overflow-Y:scroll;}.edit-box{width:100%; height:100%;}</style> <title>Khun Sangkeet Admin Controls</title> </head> <body> <nav class="navbar bg-dark bg-gradient bg-opacity-10"> <a href="/admin" class="nav-bar-content"> <h1>Khun Sangkeet E-Admin</h1> </a> <a href="/admin/logout" class="nav-bar-content"> <span class="material-symbols-outlined"> logout </span> </a> </nav> <section class="big-content"> <nav class="nav flex-column bg-dark bg-opacity-10"> <a class="nav-link" href="/admin/">Home</a> <a class="nav-link" href="/admin/config">Config</a> <a class="nav-link" href="/admin/edit">Edit</a> <a class="nav-link" href="/docs">Fastapi Docs</a> <a class="nav-link" href="/redoc">Fastapi NewDocs</a> <a class="nav-link" href="/admin/about">About</a> </nav> /*content*/ </section> <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script> </body></html>
"""

admin_login = """
<div class="ct-form"> <div> <div class="alert alert-primary" role="alert"> <h4 class="alert-heading">Where I Can Get Admin Token</h4> <p>Check In Terminal</p></div>/*err*/ <form method="post" > <h1>Login</h1> <label> Token </label> <input class="form-control" name="adminToken"/> <br/> <input type="submit" value="Login" class="btn btn-primary"/> </form> </div></div>
"""

admin_login_wrongToken = """
<div class="alert alert-danger alert-dismissible fade show" role="alert"> <strong>Wrong Token</strong> Plase Try Again. <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>
"""

admin_welcome = """
<div class="ct-form"> <div> <img width="100%" height="250px" src="https://img.freepik.com/premium-photo/welcome-different-language-paper-with-world-map-background-words-cloud-concept_505353-96.jpg"/> <div class="alert alert-success" role="alert"> <h4 class="alert-heading">Wellcome Khun Sangkeet</h4> <p>To Setup/Control panel</p><hr/> <p class="mb-0">View Project On GitHub : https://github.com/namfon00/sangkeeteffect</p></div>/*ngrokLinkBox*/ <div class="form-control"> <h2>Topic</h2> <a class="list-admin-content" href="admin"> <span class="material-symbols-outlined"> home </span> Home </a> <a class="list-admin-content" href="#"> <span class="material-symbols-outlined"> description </span> Documents </a> <a class="list-admin-content" href="admin/config"> <span class="material-symbols-outlined"> settings </span> Config </a> <a class="list-admin-content" href="admin/edit"> <span class="material-symbols-outlined"> edit </span> Edit </a> <a class="list-admin-content" href="/docs"> <img height="20px" src="https://static-00.iconduck.com/assets.00/fastapi-icon-512x512-a7ggfxfw.png"/> Fastapi Interactive API docs </a> <a class="list-admin-content" href="/redoc"> <img height="20px" src="https://static-00.iconduck.com/assets.00/fastapi-icon-512x512-a7ggfxfw.png"/> Fastapi Alternative API docs </a> <a class="list-admin-content" href="admin/edit"> <span class="material-symbols-outlined"> info </span> About </a> </div><br/><br/> <div class="form-control"> <h2>Sponsor</h2> <a class="list-admin-content" href="https://github.com/namfon00"> <span class="material-symbols-outlined"> person </span> Namfon00 </a> <a class="list-admin-content" href="https://github.com/patwora"> <span class="material-symbols-outlined"> person </span> Patwora </a> <a class="list-admin-content" href="https://github.com/EyeOnwara"> <span class="material-symbols-outlined"> person </span> EyeOnwara </a> <a class="list-admin-content" href="https://github.com/Rata-un"> <span class="material-symbols-outlined"> person </span> Rata-un </a> <a class="list-admin-content" href="https://github.com/SupaschaiPh"> <span class="material-symbols-outlined"> person </span> SupaschaiPh </a> </div></div></div>
"""

admin_welcome_showNgrokLink = """
<div class="alert alert-primary" role="alert"> <h4 class="alert-heading"> <span style="font-size:2rem;" class="material-symbols-outlined"> link </span> Ngrok Link </h4> <p>/*ngrokLink*/</p></div>
"""

admin_config = """
<div class="ct-form"> <div> <div class="alert alert-danger" role="alert"> <h4 class="alert-heading"> <span class="material-symbols-outlined"> warning </span> Danger!! </h4> <p>Change port must change in config.json!!</p><hr/> <p class="mb-0">Change Parent path must restart runtime</p></div><form method="post" class="form-control"> <h1> <span class="material-symbols-outlined"> settings </span> config </h1> <table> <tr> <td> <label>Port</label> </td><td> <input name="port" min="0" type="number" class="form-control" value="/*port*/" disabled/> </td></tr><tr> <td> <label>Parent path</label> </td><td> <input name="path" class="form-control" value="/*path*/"/> </td></tr><tr> <th> <label>Template Path</label> </th> </tr><tr> <td> <label>Home</label> </td><td> <input name="home" class="form-control" value="/*home*/"/> </td></tr><tr> <td> <label>Add Sound</label> </td><td> <input name="add sound" class="form-control" value="/*addSound*/"/> </td></tr><tr> <th> <div class="form-check form-switch"> <input class="form-check-input" type="radio" name="storageType" value="local" checked/> <label class="form-check-label"> Local Storage </label> </div></th> </tr><tr> <td> <label>Data Storage Path</label> </td><td> <input name="dataStorage" class="form-control" value="/*soundData*/"/> </td></tr><tr> <td> <label>Sound Storage Path</label> </td><td> <input name="soundStorage" class="form-control" value="/*soundStorage*/"/> </td></tr><tr> <td> <label>Cover Storage Path</label> </td><td> <input name="coverStorage" class="form-control" value="/*coverStorage*/"/> </td></tr><tr> <th> <div class="form-chec form-switch"> <input class="form-check-input" type="radio" name="storageType" value="gsheet" /*withGsheetCheck*//> <label class="form-check-label" > Storage With Gsheet </label> </div></th> </tr><tr> <td> <label>Google Form Link</label> </td><td> <input name="gFormLink" class="form-control" value="/*gFormLink*/"/> </td></tr><tr> <td> <label>Google Sheet Link</label> </td><td> <input name="sheetLink" class="form-control" value="/*sheetLink*/"/> </td></tr><tr> <td> <label>Google Sheet Link As CSV</label> </td><td> <input name="sheetLinkCSV" class="form-control" value="/*sheetLinkCSV*/"/> </td></tr><tr> <th> <div class="form-check form-switch"> <label for="flexSwitchCheckDefault">Ngrok (สำหรับแชร์ Localhost)</label> <input class="form-check-input" type="checkbox" role="switch" name="ngrok" /*ngrokCheck*//> </div></th> </tr>/*ngrokLink*/ <tr> <td> <label>Token</label> </td><td> <input class="form-control" name="ngrokToken" value="/*ngrokToken*/"/> </td></tr><tr> <td></td><td style="text-align: right"> <input value="Save" class="btn btn-success" type="submit"/> </td></tr></table> </form> </div></div>
"""

admin_edit = """
<div class='ct-form'> <style>tr{border-bottom:solid 1px var(--bs-gray-300)}</style> <div> <h1> <span class="material-symbols-outlined"> edit_square </span> Edit File/Data </h1> <div class="form-control ct-edit"> <h2> <span class="material-symbols-outlined"> folder </span> Templates </h2> <table> /*templateFiles*/ </table> </div><br/> <div class="form-control ct-edit"> <h2> <span class="material-symbols-outlined"> database </span> Sound </h2> /*soundData*/ </div></div><div>
"""

# Soon]
