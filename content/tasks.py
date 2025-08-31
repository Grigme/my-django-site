from django.db.models import F
from .models import VideoContent, AudioContent

MODEL_MAP = {
    'videocontent': VideoContent,
    'audiocontent': AudioContent,
}

def increment_counters_task(content_ids):
    for model_name, content_id in content_ids:
        model_class = MODEL_MAP.get(model_name)
        if model_class:
            model_class.objects.filter(id=content_id).update(counter=F('counter') + 1)