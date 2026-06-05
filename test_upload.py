import requests

url = 'http://127.0.0.1:8000/api/upload/'

# ชื่อ 'video_file' ต้องตรงกับที่ตั้งไว้ใน models.py
# เปลี่ยน 'sample.mp4' เป็นชื่อไฟล์วิดีโอที่มีในเครื่องคุณ
files = {'video_file': open('sample.mp4', 'rb')} 
data = {'title': 'วิดีโอทดสอบจากสคริปต์ Python'}

print("กำลังส่งไฟล์...")
response = requests.post(url, files=files, data=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")