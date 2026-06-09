import threading
from django.shortcuts import render
import os
from rest_framework import status,  generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Video, JamSession
from .serializers import VideoSerializer, JamSessionSerializer
from .youtube_api import upload_video_to_youtube

def background_youtube_upload(video_id):
    try:
        print(f"[Background Task] เริ่มอัปโหลดวิดีโอ ID: {video_id} ขึ้น YouTube...")
        
        # ดึงข้อมูลจาก Database
        video = Video.objects.get(pk=video_id)
        file_path = video.video_file.path
        video_title = video.title
        video_desc = video.description or "อัปโหลดผ่านระบบ Fuzik Connect"

        # ส่งไฟล์ขึ้น YouTube
        youtube_id = upload_video_to_youtube(file_path, video_title, video_desc)
        
        # อัปเดต ID กลับลง Database
        video.youtube_id = youtube_id
        video.save()
        
        print(f"[Background Task] อัปโหลดสำเร็จ! YouTube ID: {youtube_id}")
    except Exception as e:
        print(f"[Background Task] อัปโหลดพลาดสำหรับ ID {video_id}: {e}")


class VideoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = VideoSerializer(data=request.data)
        
        if file_serializer.is_valid():
            video_instance = file_serializer.save()
            
            upload_thread = threading.Thread(
                target=background_youtube_upload,
                args=(video_instance.id,)
            )
            upload_thread.start() 

            response_data = VideoSerializer(video_instance).data
            response_data['message'] = "รับไฟล์เรียบร้อย กำลังดำเนินการอัปโหลดขึ้น YouTube เบื้องหลัง..."
            return Response(response_data, status=status.HTTP_201_CREATED)
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
        
        if video.youtube_id:
            return Response({'status': 'error', 'message': 'วิดีโอนี้อยู่บน YouTube แล้ว'}, status=status.HTTP_400_BAD_REQUEST)

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