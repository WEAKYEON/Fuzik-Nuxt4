from django.db import models

class Video(models.Model): 
    # ตัวเลือก (Choices) สำหรับประเภทวิดีโอ
    VIDEO_TYPES = (
        ('solo', 'Solo'),
        ('collab', 'Collaboration'),
    )
    
    # ตัวเลือกสถานะการอัปโหลด YouTube
    YOUTUBE_STATUS_CHOICES = (
        ('none', 'ยังไม่อัปโหลด'),
        ('pending', 'กำลังรอคิวอัปโหลด'),
        ('completed', 'อัปโหลดเสร็จสิ้น'),
        ('failed', 'อัปโหลดล้มเหลว'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_file = models.FileField(upload_to='temp_videos/')
    youtube_id = models.CharField(max_length=50, blank=True, null=True)
    
    # เก็บประเภทวิดีโอ (ค่าเริ่มต้นให้เป็น solo)
    video_type = models.CharField(max_length=10, choices=VIDEO_TYPES, default='solo')
    
    # เก็บสถานะเพื่อเอาไปทำ Batch Job
    youtube_status = models.CharField(max_length=20, choices=YOUTUBE_STATUS_CHOICES, default='none')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class JamSession(models.Model):
    layout = models.CharField(max_length=50) 
    tracks = models.JSONField(default=list) 
    status = models.CharField(max_length=20, default='pending') 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Jam {self.id} - {self.layout} ({self.status})"