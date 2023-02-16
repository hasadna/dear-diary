from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Calendar(BaseModel):
    resource_id = models.UUIDField(db_index=True, unique=True)
    title = models.CharField(max_length=100)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
        }


class Event(BaseModel):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    subject = models.CharField(max_length=250)
    location = models.CharField(max_length=50, null=True)

    # https://stackoverflow.com/questions/45328826/django-model-fields-indexing
    class Meta:
        indexes = [
            models.Index(fields=['calendar','start',]),
        ]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.subject,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
        }
