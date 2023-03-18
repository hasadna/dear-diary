from django.db import models
from django.utils import timezone
from django.db.models import CheckConstraint, Q, F


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Calendar(BaseModel):
    resource_id = models.UUIDField(db_index=True, unique=True)
    title = models.CharField(max_length=300)
    when_created_at_source = models.DateTimeField(null=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
        }

    def __str__(self):
        return f"{self.title} ({self.resource_id})"


class DownloadReport(BaseModel):
    """
    Reporting on a download attempt
    """
    resource_id = models.UUIDField(db_index=True)
    status = models.CharField(max_length=15)
    detail = models.TextField(null=True)

    def __str__(self):
        return f"{self.resource_id} ({self.created_at}): {self.status}"


class Event(BaseModel):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    subject = models.CharField(max_length=600)
    location = models.CharField(max_length=50, null=True)

    # https://stackoverflow.com/questions/45328826/django-model-fields-indexing
    class Meta:
        indexes = [
            models.Index(fields=['calendar','start',]),
        ]
        constraints = [
            CheckConstraint(
                check = Q(end__gt=F('start')),
                name = 'end_after_start',
            ),
        ]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.subject,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "location": self.location,
        }

    def __str__(self):
        return f"{self.subject}: {self.start}-{self.end}"
