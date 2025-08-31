from django.test import TestCase
from ..models import Page, VideoContent, AudioContent

class TaskFunctionTest(TestCase):
    def test_increment_counters_task(self):
        """Test that increment_counters_task works correctly"""
        from ..tasks import increment_counters_task
        
        page = Page.objects.create(title="Task Test Page")
        video = VideoContent.objects.create(
            page=page,
            title="Task Video",
            video_url="https://example.com/task.mp4",
            counter=10,
            order=1
        )
        audio = AudioContent.objects.create(
            page=page,
            title="Task Audio",
            text="Task text",
            counter=5,
            order=2
        )
        
        content_ids = [
            ('videocontent', video.id),
            ('audiocontent', audio.id)
        ]
        
        increment_counters_task(content_ids)
        
        video.refresh_from_db()
        audio.refresh_from_db()
        
        self.assertEqual(video.counter, 11)
        self.assertEqual(audio.counter, 6)
    
    def test_increment_counters_task_unknown_model(self):
        """Test that task handles unknown model names gracefully"""
        from ..tasks import increment_counters_task
        
        content_ids = [('unknownmodel', 999)]
        
        try:
            increment_counters_task(content_ids)
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)