from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.title

class BaseContent(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=255)
    counter = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.page.title})"

class VideoContent(BaseContent):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='video_contents')
    video_url = models.URLField()
    subtitles_url = models.URLField(blank=True, null=True)

class AudioContent(BaseContent):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='audio_contents')
    text = models.TextField()