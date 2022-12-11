# สังคีตเอฟเฟกต์<img width="50" src="https://media.tenor.com/8McIGu0Tf_QAAAAi/fire-joypixels.gif" />

![](https://github.com/SupaschaiPh/SupaschaiPh/blob/main/badges/KMITL-5.svg) ![](https://github.com/SupaschaiPh/SupaschaiPh/blob/main/badges/IT-1.svg)


# สังคีตเอฟเฟกต์คืออะไร ?
สังคีตเอฟเฟกต์ คือ เว็บในการเล่นเสียงและเก็บรวมรวมเสียงสังคีตเอฟเฟกต์ต่างๆ ที่มีระบบการจัดการ โดยสามารถรับข้อมูลไฟล์ได้จากในเครื่อง หรือ รับจากกูเกิลชีตและกูเกิลฟอร์ม อีกทั้งยังมีระบบแชร์หน้าไปให้ผู้อื่นใช้ได้ด้วย 
สังคีตเอฟเฟกต์มี 2 ส่วนใหญ่ๆ 
* ส่วนผู้ใช้ 
  * หน้าสำหรับแสดงเสียงทั้งหมด 
  * หน้าสำหรับเพิ่มเสียง(ถ้าใช้โหมด Google Sheet จะถูกเปลี่ยนเป็น Google From)
  * หน้าแสดงรายละเอียดข้อมูลเสียง
  * หน้าแสดงผลการค้นหาเสียง
* ส่วนผู้ดูแล(ตัวระบบการจัดการ)ประกอบด้วย 
  * หน้าล็อกอิน
  * หน้าต้อนรับผู้ดูแล
  * หน้าConfigสำหรับตั้งค่าหรือเปิดใช้ฟังก์ชั่นต่างๆ เช่น การเลือกจะใช้การจัดเก็บข้อมูลแบบในเครื่อง หรือ Google From และ Google Sheet
  * หน้า Edit จะมีสองส่วนใหญ่ๆ คือส่วนในการแก้ไข้ Templates ของผู้ใช้ และส่วนแก้ไข้ข้อมูลของเสียง(ถ้าใช้โหมด Google Sheet จะเป็นแค่การแสดงตารางเท่านั้นถ้าต้องการแก้ต้องแก้ในGoogle Sheet)
* ส่วนเพิ่มเติม
  * หน้าSwagger UI
  * หน้าAlternative API documentation
# วิธีการใช้quickstart
1.เปลี่ยน directory 
``` 
cd {path ของโฟลเดอร์ sangkeeteffect}
```

2.โหลด Requirements 
```
pip install -r requirements.txt
```
3.รัน app ด้วยคำสั่งด้านล่างนี้
```
python3 {path ของ main_app.py}
```
# ความต้องการ
* python 3.10 ++
* fastapi == 0.86.0
* uvicorn[standard] == 0.19.0
* python-multipart == 0.0.5
* pyngrok == 5.1.0
* pandas
# ไฟล์/โฟลเดอร์
* การเปลี่ยนที่อยู่ของไฟล์
ห้ามเปลี่ยนที่อยู่ของไฟล์ หรือ โฟรเดอร์ตามรายการที่มี*โดยเด็ดขาดต่อไปนี้!!
```
sangkeeteffect
│   .DS_Store
│   main_app.py*
│   README.md
│   requirements.txt*
│
│
├───admin_templates*
│       admin-config.txt*
│       admin-edit-dataSound.txt*
│       admin-edit-dataSoundRow.txt*
│       admin-edit-editSoundData.txt*
│       admin-edit-textarea.txt*
│       admin-edit.txt*
│       admin-login-wrongToken.txt*
│       admin-login.txt*
│       admin-tem.txt*
│       admin-welcome-showNgrokLink.txt*
│       admin-welcome.txt*
│
├───data*
│   │   config.json*
│   │   sound_data.json*
│   │
│   └───sound*
│
│
├───modules*
│   │   CheckRequireFile.py*
│   │   KhunSangkeetE_Admin.py*
│   │   KhunSangkeetE_User.py*
│   │
│
└───templates*
        404.html
        add_sound.html
        home.html
        info.html

```


# ฟังก์ชั่น
+ ฟังก์ชั่นNgrok ต้องใส่ Ngrok Token(หาได้จาก https://dashboard.ngrok.com/) จึงจะใช้งานได้
# ผู้จัดทำ 
1. 65070195 นางสาวรตา อุณหะ

2. 65070203 นางสาววรดา สาระคนธ์

3. 65070237 นางสาวสิริทัต จงศิริ 

4. 65070242 นายสุภัศชัย โพธิชัย 

5. 65070252 นางสาวอรวรา หงษ์เผือก 

