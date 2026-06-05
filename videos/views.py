from django.shortcuts import render
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view # 📌 1. นำเข้า api_view สำหรับฟังก์ชันใหม่
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Video # 📌 2. ดึง Model มาไว้ข้างบนสุดเลยจะได้ใช้ได้ทุกที่
from .serializers import VideoSerializer
from .youtube_api import upload_video_to_youtube

class VideoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = VideoSerializer(data=request.data)
        
        if file_serializer.is_valid():
            video_instance = file_serializer.save()
            
            try:
                # file_path = video_instance.video_file.path
                # video_title = video_instance.title

                # # ส่งไฟล์ขึ้น YouTube
                # youtube_id = upload_video_to_youtube(file_path, video_title, video_instance.description)
                
                # # เอารหัสมาเซฟทับ
                # video_instance.youtube_id = youtube_id
                # video_instance.save()

                response_data = VideoSerializer(video_instance).data
                return Response(response_data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all().order_by('-uploaded_at')
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def push_to_youtube(request, pk):
    try:
        video = Video.objects.get(pk=pk)
        
        # ป้องกันการอัปโหลดซ้ำ
        if video.youtube_id:
            return Response({'status': 'error', 'message': 'วิดีโอนี้อยู่บน YouTube แล้ว'}, status=400)

        file_path = video.video_file.path
        
        # เรียกใช้สคริปต์ YouTube
        youtube_id = upload_video_to_youtube(
            file_path=file_path, 
            title=video.title, 
            description=video.description or "อัปโหลดผ่านระบบ Fuzik Connect"
        )
        
        # อัปเดต ID กลับลง Database
        video.youtube_id = youtube_id
        video.save()

        return Response({'status': 'success', 'youtube_id': youtube_id})
    
    except Video.DoesNotExist:
        return Response({'status': 'error', 'message': 'ไม่พบวิดีโอนี้ในระบบ'}, status=404)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)