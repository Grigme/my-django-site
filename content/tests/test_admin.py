from django.test import TestCase
from ..models import Page, VideoContent, AudioContent

class AdminTest(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="Admin Test Page")
        self.video = VideoContent.objects.create(
            page=self.page,
            title="Admin Video",
            video_url="https://example.com/admin.mp4",
            order=1
        )
        self.audio = AudioContent.objects.create(
            page=self.page,
            title="Admin Audio",
            text="Admin audio text",
            order=2
        )

    def test_page_admin_display(self):
        from django.contrib.admin.sites import site
        
        self.assertTrue(site.is_registered(Page))
        self.assertTrue(site.is_registered(VideoContent))
        self.assertTrue(site.is_registered(AudioContent))

    def test_page_admin_search(self):
        pages = Page.objects.filter(title__istartswith='Admin')
        self.assertEqual(pages.count(), 1)
        self.assertEqual(pages.first().title, "Admin Test Page")