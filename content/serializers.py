from rest_framework import serializers
from .models import Page, VideoContent, AudioContent

class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = '__all__'

class AudioContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioContent
        fields = '__all__'

class ContentSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj.__class__.__name__.lower()

    def get_data(self, obj):
        if isinstance(obj, VideoContent):
            return VideoContentSerializer(obj).data
        elif isinstance(obj, AudioContent):
            return AudioContentSerializer(obj).data
        return None

class PageListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='page-detail', read_only=True)

    class Meta:
        model = Page
        fields = ['id', 'title', 'url']

class PageDetailSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['id', 'title', 'contents']

    def get_contents(self, obj):
        all_content = []
        for video in obj.video_contents.all():
            all_content.append(video)
        for audio in obj.audio_contents.all():
            all_content.append(audio)
        # Сортируем объединенный список по полю `order`
        all_content_sorted = sorted(all_content, key=lambda x: x.order)
        return ContentSerializer(all_content_sorted, many=True).data