import threading
import os
import random
import string

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Video, JamSession
from .serializers import VideoSerializer, JamSessionSerializer
from .youtube_api import upload_video_to_youtube

# -------------------------------------------------------------------
# 1. ระบบเบื้องหลังสำหรับอัปโหลดขึ้น YouTube (เก็บไว้เผื่อแอดมินกดสั่งงาน)
# -------------------------------------------------------------------
def background_youtube_upload(video_id):
    try:
        video = Video.objects.get(pk=video_id)
        video.youtube_status = 'uploading'
        video.save()
        
        print(f"[Background Task] เริ่มอัปโหลดวิดีโอ ID: {video_id} ขึ้น YouTube...")
        
        file_path = video.video_file.path
        video_title = video.title
        video_desc = video.description or "อัปโหลดผ่านระบบ Fuzik Connect"

        youtube_id = upload_video_to_youtube(file_path, video_title, video_desc)
        
        video.youtube_id = youtube_id
        video.youtube_status = 'completed'
        video.save()
        
        print(f"[Background Task] อัปโหลดสำเร็จ! YouTube ID: {youtube_id}")
    except Exception as e:
        print(f"[Background Task] อัปโหลดพลาดสำหรับ ID {video_id}: {e}")
        video = Video.objects.get(pk=video_id)
        video.youtube_status = 'failed'
        video.save()

# -------------------------------------------------------------------
# รับไฟล์จากหน้าเว็บ Nuxt (พักไว้ก่อน ไม่ลงสุ่มสี่สุ่มห้า)
# -------------------------------------------------------------------
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_video(request):
    video_file = request.FILES.get('video_file')
    title = request.data.get('title', 'Untitled Video')
    description = request.data.get('description', '')    
    video_type = request.data.get('video_type', 'solo')  

    if not video_file:
        return Response({"error": "ไม่พบไฟล์วิดีโอ กรุณาอัปโหลดใหม่"}, status=400)

    # สร้าง Fuzik URL สุ่ม
    random_url = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    new_video = Video.objects.create(
        title=title,
        description=description, 
        video_type=video_type,   
        fuzik_url=random_url,
        video_file=video_file,
        youtube_status='none'    #บังคับเป็น 'none' ให้รอแอดมินตรวจ
    )

    return Response({
        "message": "อัปโหลดเข้าเซิร์ฟเวอร์สำเร็จ! รอการตรวจสอบ",
        "video_url": new_video.fuzik_url
    }, status=201)

# -------------------------------------------------------------------
# 3. API สำหรับดึงข้อมูลและจัดการอื่นๆ (คงของเก่าไว้ทั้งหมด)
# -------------------------------------------------------------------
class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all().order_by('-uploaded_at')
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def push_to_youtube(request, pk):
    try:
        video = Video.objects.get(pk=pk)
        
        if video.youtube_id or video.youtube_status in ['pending', 'completed']:
            return Response({'status': 'error', 'message': 'วิดีโอนี้อยู่บน YouTube หรือกำลังรอคิวอยู่แล้ว'}, status=status.HTTP_400_BAD_REQUEST)

        video.youtube_status = 'pending'
        video.save()

        upload_thread = threading.Thread(
            target=background_youtube_upload,
            args=(video.id,)
        )
        upload_thread.start()

        return Response({
            'status': 'success', 
            'message': 'รับคำสั่งเรียบร้อย กำลังดำเนินการดันขึ้น YouTube เบื้องหลัง...'
        }, status=status.HTTP_202_ACCEPTED)
    
    except Video.DoesNotExist:
        return Response({'status': 'error', 'message': 'ไม่พบวิดีโอนี้ในระบบ'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class JamSessionCreateView(APIView):
    def get(self, request, *args, **kwargs):
        sessions = JamSession.objects.all().order_by('-id')
        serializer = JamSessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = JamSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class JamSessionDetailView(generics.RetrieveAPIView):
    queryset = JamSession.objects.all()
    serializer_class = JamSessionSerializer