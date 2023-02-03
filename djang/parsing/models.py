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


class Event(BaseModel):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    subject = models.CharField(max_length=50)
    location = models.CharField(max_length=50, null=True)
