import os
import django
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# 1. Setup สภาพแวดล้อม Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuzik_backend.settings') # ปลี่ยนชื่อโปรเจกต์ของคุณตรงนี้
django.setup()

from videos.models import Video # เปลี่ยนชื่อแอปของคุณตรงนี้

# ตั้งค่าสิทธิ์ (Scope) สำหรับอัปโหลดวิดีโอ YouTube
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_youtube_service():
    creds = None
    # ไฟล์ token.pickle จะเก็บ Credentials หลังจากล็อกอินครั้งแรกเสร็จแล้ว
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # ถ้าไม่มี Token หรือ Token หมดอายุ ให้ทำการล็อกอินใหม่
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # สคริปต์จะอ่านไฟล์ client_secret.json ที่โหลดมาจาก Google Cloud
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # เซฟ Token เก็บไว้ใช้ครั้งต่อไปแบบเงียบๆ (ไม่ต้องล็อกอินซ้ำ)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)

def process_batch_upload():
    youtube = get_youtube_service()
    
    # 2. ดึงวิดีโอที่มีสถานะ 'pending' (แอดมินกดอนุมัติ/สั่งให้เข้าคิวอัปโหลดแล้ว)
    queue_videos = Video.objects.filter(youtube_status='pending')
    
    if not queue_videos.exists():
        print("ไม่มีวิดีโอค้างอยู่ในคิวอัปโหลด")
        return

    for video in queue_videos:
        print(f"กำลังเริ่มอัปโหลดวิดีโอ: {video.title}")
        
        # เปลี่ยนสถานะใน DB เป็นกำลังอัปโหลด เพื่อไม่ให้เกิดการทำงานซ้ำ
        video.youtube_status = 'uploading'
        video.save()

        try:
            # ดึง Path ของไฟล์วิดีโอจริงในเซิร์ฟเวอร์
            file_path = video.video_file.path
            
            # ตั้งค่า Metadata สำหรับ YouTube
            body = {
                'snippet': {
                    'title': video.title,
                    'description': video.description or 'Uploaded via Fuzik Connect',
                    'tags': ['fuzik', 'music', 'cover'],
                    'categoryId': '10' # หมวดหมู่เพลง (Music)
                },
                'status': {
                    'privacyStatus': 'unlisted' # อัปโหลดเป็น Unlisted ไว้ก่อนเพื่อความปลอดภัย
                }
            }

            # เตรียมไฟล์สำหรับการส่งข้อมูล (ในที่นี้คือไฟล์วิดีโอที่เราเซฟในโฟลเดอร์)
            media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype='video/*')
            
            # สั่งยิง API ขึ้น YouTube
            request = youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            print(f"กำลังส่งไฟล์ขึ้น YouTube...")
            response = request.execute()
            
            # 3. โจทย์: เพิ่ม URL ของ YouTube มาคู่กับวิดีโอเดิม
            # เมื่ออัปโหลดสำเร็จดึง youtube_id มาบันทึก และเปลี่ยนสถานะเป็น completed
            video.youtube_id = response['id']
            video.youtube_status = 'completed'
            video.save()
            
            print(f"อัปโหลดสำเร็จ! ได้ YouTube ID: {response['id']}")

        except Exception as e:
            print(f"อัปโหลดล้มเหลวสำหรับวิดีโอ {video.title}: {e}")
            video.youtube_status = 'failed'
            video.save()

if __name__ == '__main__':
    process_batch_upload()