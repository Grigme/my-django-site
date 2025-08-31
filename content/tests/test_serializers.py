from rest_framework.test import APIRequestFactory
from django.test import TestCase
from ..models import Page, VideoContent, AudioContent

class SerializersTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/')
        self.page = Page.objects.create(title="Test Serializer Page")
        self.video = VideoContent.objects.create(
            page=self.page,
            title="Video Serializer",
            video_url="https://example.com/video.mp4",
            order=1
        )
        self.audio = AudioContent.objects.create(
            page=self.page,
            title="Audio Serializer",
            text="Serializer text",
            order=2
        )

    def test_video_content_serializer(self):
        from ..serializers import VideoContentSerializer
        
        serializer = VideoContentSerializer(self.video)
        data = serializer.data
        
        self.assertEqual(data['title'], "Video Serializer")
        self.assertEqual(data['video_url'], "https://example.com/video.mp4")
        self.assertEqual(data['page'], self.page.id)
        self.assertEqual(data['order'], 1)
        self.assertEqual(data['counter'], 0)

    def test_audio_content_serializer(self):
        from ..serializers import AudioContentSerializer
        
        serializer = AudioContentSerializer(self.audio)
        data = serializer.data
        
        self.assertEqual(data['title'], "Audio Serializer")
        self.assertEqual(data['text'], "Serializer text")
        self.assertEqual(data['page'], self.page.id)
        self.assertEqual(data['order'], 2)
        self.assertEqual(data['counter'], 0)

    def test_content_serializer_type_detection(self):
        from ..serializers import ContentSerializer
        
        video_serializer = ContentSerializer(self.video)
        self.assertEqual(video_serializer.data['type'], 'videocontent')
        
        audio_serializer = ContentSerializer(self.audio)
        self.assertEqual(audio_serializer.data['type'], 'audiocontent')

    def test_page_list_serializer(self):
        from ..serializers import PageListSerializer
        
        serializer = PageListSerializer(self.page, context={'request': self.request})
        data = serializer.data
        
        self.assertEqual(data['title'], "Test Serializer Page")
        self.assertIn('url', data)