# content/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase

from ..models import Page, VideoContent, AudioContent
from ..views import StandardPagination


class HomeViewTest(TestCase):
    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['message'], 'CMS API is running!')
        self.assertIn('pages_list', response_data['endpoints'])
        self.assertIn('admin_panel', response_data['endpoints'])


class PageViewSetTest(APITestCase):
    def setUp(self):
        self.page1 = Page.objects.create(title="Page 1")
        self.page2 = Page.objects.create(title="Page 2")
        self.page3 = Page.objects.create(title="Page 3")
        
        self.video1 = VideoContent.objects.create(
            page=self.page1,
            title="Video 1",
            video_url="https://example.com/video1.mp4",
            order=2
        )
        self.video2 = VideoContent.objects.create(
            page=self.page1,
            title="Video 2",
            video_url="https://example.com/video2.mp4",
            order=1
        )
        
        self.audio1 = AudioContent.objects.create(
            page=self.page1,
            title="Audio 1",
            text="Audio text 1",
            order=3
        )
        
        VideoContent.objects.create(
            page=self.page2,
            title="Video Page 2",
            video_url="https://example.com/video3.mp4",
            order=1
        )

    def test_page_list(self):
        url = reverse('page-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        
        expected_page_size = StandardPagination.page_size
        self.assertEqual(len(response.data['results']), min(3, expected_page_size))
        
        self.assertEqual(response.data['results'][0]['title'], "Page 1")
        self.assertIn('url', response.data['results'][0])

    def test_page_list_pagination(self):
        for i in range(10):
            Page.objects.create(title=f"Extra Page {i+1}")
        
        url = reverse('page-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_page_size = StandardPagination.page_size
        total_count = Page.objects.count()
        
        self.assertEqual(response.data['count'], total_count)
        self.assertEqual(len(response.data['results']), min(total_count, expected_page_size))

    def test_page_detail(self):
        url = reverse('page-detail', kwargs={'pk': self.page1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Page 1")
        self.assertEqual(len(response.data['contents']), 3)
        
        self.assertEqual(response.data['contents'][0]['type'], 'videocontent')
        self.assertEqual(response.data['contents'][0]['data']['title'], "Video 2")
        
        self.assertEqual(response.data['contents'][1]['type'], 'videocontent')
        self.assertEqual(response.data['contents'][1]['data']['title'], "Video 1")
        
        self.assertEqual(response.data['contents'][2]['type'], 'audiocontent')
        self.assertEqual(response.data['contents'][2]['data']['title'], "Audio 1")

    def test_page_detail_not_found(self):
        url = reverse('page-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_page_detail_content_types(self):
        url = reverse('page-detail', kwargs={'pk': self.page1.pk})
        response = self.client.get(url)
        
        video_content = next((c for c in response.data['contents'] if c['type'] == 'videocontent'), None)
        self.assertIsNotNone(video_content)
        self.assertIn('video_url', video_content['data'])
        self.assertIn('subtitles_url', video_content['data'])
        
        audio_content = next((c for c in response.data['contents'] if c['type'] == 'audiocontent'), None)
        self.assertIsNotNone(audio_content)
        self.assertIn('text', audio_content['data'])


class CounterIncrementTest(APITestCase):
    def setUp(self):
        self.page = Page.objects.create(title="Test Counter Page")
        self.video = VideoContent.objects.create(
            page=self.page,
            title="Test Video Counter",
            video_url="https://example.com/video.mp4",
            counter=5,
            order=1
        )
        self.audio = AudioContent.objects.create(
            page=self.page,
            title="Test Audio Counter",
            text="Test text",
            counter=3,
            order=2
        )

    def test_counter_values_before_retrieve(self):
        """Test that counters have initial values"""
        self.video.refresh_from_db()
        self.audio.refresh_from_db()
        self.assertEqual(self.video.counter, 5)
        self.assertEqual(self.audio.counter, 3)

    def test_page_retrieval_works(self):
        """Test that page retrieval works correctly"""
        url = reverse('page-detail', kwargs={'pk': self.page.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Counter Page")
        self.assertEqual(len(response.data['contents']), 2)


class PaginationTest(APITestCase):
    def setUp(self):
        for i in range(10):
            Page.objects.create(title=f"Page {i+1}")
    
    def test_custom_page_size(self):
        """Test custom page size parameter"""
        url = reverse('page-list') + '?page_size=5'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['count'], 10)
    
    def test_max_page_size(self):
        """Test that max_page_size is enforced"""
        url = reverse('page-list') + '?page_size=200'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data['results']), StandardPagination.max_page_size)


class ContentOrderingTest(APITestCase):
    def test_content_ordering_across_types(self):
        """Test that content from different types is properly ordered together"""
        page = Page.objects.create(title="Ordering Test Page")
        
        AudioContent.objects.create(
            page=page,
            title="Audio Late",
            text="Text",
            order=5
        )
        VideoContent.objects.create(
            page=page,
            title="Video Early",
            video_url="https://example.com/early.mp4",
            order=1
        )
        AudioContent.objects.create(
            page=page,
            title="Audio Middle",
            text="Text",
            order=3
        )
        VideoContent.objects.create(
            page=page,
            title="Video Middle",
            video_url="https://example.com/middle.mp4",
            order=2
        )
        
        url = reverse('page-detail', kwargs={'pk': page.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['contents']), 4)
        
        self.assertEqual(response.data['contents'][0]['data']['title'], "Video Early")
        self.assertEqual(response.data['contents'][1]['data']['title'], "Video Middle")
        self.assertEqual(response.data['contents'][2]['data']['title'], "Audio Middle")
        self.assertEqual(response.data['contents'][3]['data']['title'], "Audio Late")


class ErrorHandlingTest(APITestCase):
    def test_nonexistent_page_detail(self):
        """Test handling of non-existent page in detail view"""
        url = reverse('page-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)