import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def upload_video_to_youtube(file_path, title, description="อัปโหลดผ่านระบบ Fuzik Connect"):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    
    # 📌 1. บังคับพิกัดไฟล์ให้อยู่ที่เดียวกับ manage.py เสมอ จะได้หาเจอตลอด
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    client_secrets_file = os.path.join(BASE_DIR, 'client_secrets.json')
    token_file = os.path.join(BASE_DIR, 'token.json')

    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            # 📌 2. เพิ่ม prompt='consent' เพื่อบังคับให้ Google แจก Refresh Token แน่นอน
            creds = flow.run_local_server(port=0, prompt='consent')
            
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    print(f"กำลังอัปโหลดวิดีโอ: {title} ...")
    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": title,
            "description": description,
            "tags": ["Fuzik", "System"],
            "categoryId": "22"
          },
          "status": {
            "privacyStatus": "unlisted"
          }
        },
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    
    response = request.execute()
    print(f"อัปโหลดสำเร็จอัตโนมัติ! Video ID: {response['id']}")
    
    return response['id']