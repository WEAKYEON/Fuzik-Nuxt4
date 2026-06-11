import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuzik_backend.settings')
django.setup()

from videos.models import Video

def fetch_and_sync_real_videos():
    api_url = "https://fuzik03.tetraserver.com/plays_l/"
    print("กำลังดึงข้อมูลจากเว็บจริง...")
    
    try:
        response = requests.get(api_url)
        videos_data = response.json()
        
        media_path = os.path.join('media', 'temp_videos')
        os.makedirs(media_path, exist_ok=True)

        for item in videos_data:
            # ข้ามถ้าวิดีโอมีในฐานข้อมูลแล้ว
            if Video.objects.filter(fuzik_url=item['url']).exists():
                continue
                
            print(f"กำลังดูดคลิป: {item['video_title']}")
            
            # 1. ทริค: เดา URL ของวิดีโอจาก URL ของรูปภาพ
            preview_url = item.get('preview', '')
            video_url = preview_url.replace('.png', '.mp4').replace('.jpg', '.mp4')
            
            filename = f"{item['url']}_video.mp4"
            file_path = os.path.join(media_path, filename)
            
            # 2. ทำการดาวน์โหลดไฟล์วิดีโอจริง
            try:
                # ใช้ stream=True เพื่อค่อยๆ โหลดไฟล์ทีละส่วน (ไม่ให้ Ram เต็ม)
                video_res = requests.get(video_url, stream=True)
                
                if video_res.status_code == 200:
                    print(f"  -> กำลังโหลดไฟล์จริงขนาด {len(video_res.content) // (1024*1024) if not video_res.headers.get('content-length') else int(video_res.headers.get('content-length')) // (1024*1024)} MB...")
                    with open(file_path, 'wb') as f:
                        for chunk in video_res.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print("  -> โหลดไฟล์วิดีโอเสร็จเรียบร้อย!")
                else:
                    # ถ้าหาไฟล์ .mp4 ไม่เจอ ให้สร้างไฟล์เปล่าๆ ไว้กันระบบพัง
                    print(f"  -> หาไฟล์จริงไม่เจอ (Status {video_res.status_code}) สร้างไฟล์จำลองแทน")
                    with open(file_path, 'wb') as f:
                        f.write(b'')
            except Exception as e:
                print(f"  -> โหลดไฟล์ไม่สำเร็จ: {e}")
                with open(file_path, 'wb') as f:
                    f.write(b'')
            
            # 3. บันทึกลงฐานข้อมูล
            Video.objects.create(
                title=item['video_title'],
                description=f"เพลง: {item['music_title']} | ศิลปิน: {item['musician_name']}",
                fuzik_url=item['url'],
                video_file=f"temp_videos/{filename}",
                video_type='solo',
                youtube_status='none'
            )
            
        print("ดำเนินการดูดข้อมูลทั้งหมดเสร็จสมบูรณ์!")
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == '__main__':
    fetch_and_sync_real_videos()