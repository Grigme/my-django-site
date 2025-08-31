from django.test import TestCase
from ..models import Page, VideoContent, AudioContent

class PageModelTest(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="Test Page")
    
    def test_page_creation(self):
        self.assertEqual(self.page.title, "Test Page")
        self.assertEqual(str(self.page), "Test Page")

class VideoContentModelTest(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="Test Page")
        self.video_content = VideoContent.objects.create(
            page=self.page,
            title="Test Video",
            video_url="https://example.com/video.mp4",
            order=1
        )
    
    def test_video_content_creation(self):
        self.assertEqual(self.video_content.title, "Test Video")
        self.assertEqual(self.video_content.video_url, "https://example.com/video.mp4")
        self.assertEqual(self.video_content.counter, 0)
        self.assertEqual(str(self.video_content), "Test Video (Test Page)")

class AudioContentModelTest(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="Test Page")
        self.audio_content = AudioContent.objects.create(
            page=self.page,
            title="Test Audio",
            text="This is audio text",
            order=2
        )
    
    def test_audio_content_creation(self):
        self.assertEqual(self.audio_content.title, "Test Audio")
        self.assertEqual(self.audio_content.text, "This is audio text")
        self.assertEqual(self.audio_content.counter, 0)
        self.assertEqual(str(self.audio_content), "Test Audio (Test Page)")

class RelatedNameTest(TestCase):
    def test_related_names(self):
        """Test that related names work correctly"""
        page = Page.objects.create(title="Related Name Test")
        
        video = VideoContent.objects.create(
            page=page,
            title="Test Video",
            video_url="https://example.com/video.mp4",
            order=1
        )
        audio = AudioContent.objects.create(
            page=page,
            title="Test Audio",
            text="Test text",
            order=2
        )
        
        self.assertEqual(page.video_contents.count(), 1)
        self.assertEqual(page.video_contents.first(), video)
        
        self.assertEqual(page.audio_contents.count(), 1)
        self.assertEqual(page.audio_contents.first(), audio)

class ModelMetaTest(TestCase):
    def test_base_content_meta(self):
        """Test that BaseContent abstract model has correct Meta options"""
        from ..models import BaseContent
        
        self.assertEqual(BaseContent._meta.ordering, ['order'])
        self.assertTrue(BaseContent._meta.abstract)