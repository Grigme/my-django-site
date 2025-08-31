from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_q.tasks import async_task
from django.http import JsonResponse
from django.views import View
from .models import Page
from .serializers import PageListSerializer, PageDetailSerializer
from .tasks import increment_counters_task


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.all().prefetch_related('video_contents', 'audio_contents').order_by('id')
    pagination_class = StandardPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return PageListSerializer
        return PageDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Фоновая задача для увеличения счетчиков
        content_ids = []
        for video in instance.video_contents.all():
            content_ids.append(('videocontent', video.id))
        for audio in instance.audio_contents.all():
            content_ids.append(('audiocontent', audio.id))

        # Помещаем задачу в очередь
        async_task(increment_counters_task, content_ids)

        return Response(serializer.data)
    
class HomeView(View):
    def get(self, request):
        return JsonResponse({
            'message': 'CMS API is running!',
            'endpoints': {
                'pages_list': '/api/pages/',
                'admin_panel': '/admin/',
                'api_documentation': 'See API endpoints at /api/pages/'
            }
        })