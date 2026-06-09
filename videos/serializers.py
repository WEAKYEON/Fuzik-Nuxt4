from rest_framework import serializers
from .models import Video, JamSession

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_file', 'youtube_id', 'video_type', 'uploaded_at', 'youtube_status']
        
class JamSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JamSession
        fields = '__all__'