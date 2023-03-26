from django.db import models
from django.utils import timezone
from django.db.models import CheckConstraint, Q, F

from urllib.parse import urlencode
from django.urls import reverse


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Calendar(BaseModel):
    resource_id = models.UUIDField(db_index=True, unique=True)
    package_id = models.UUIDField()
    title = models.CharField(max_length=300)
    when_created_at_source = models.DateTimeField(null=True)

    def get_start(self):
        event = self.event_set.order_by('start').first()
        if not event:
            return None
        return event.start

    def get_end(self):
        event = self.event_set.order_by('-end').first()
        if not event:
            return None
        return event.end

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
        }

    def __str__(self):
        return f"{self.title} ({self.resource_id})"

    def get_view_url(self):
        return f"https://www.odata.org.il/dataset/{self.package_id}/resource/{self.resource_id}"

    def get_calendar_url(self, when=None):
        # TODO unfinished
        base_url = reverse("home")
        # Add fragments
        fragments = {
            "sources": self.id,
        }
        if when:
            fragments['date'] = when.strftime('%Y-%m-%d')
        url_fragment = urlencode(fragments)

        return f"{base_url}#{url_fragment}"



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
    location = models.CharField(max_length=50, null=True, blank=True)

    # https://stackoverflow.com/questions/45328826/django-model-fields-indexing
    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "calendar",
                    "start",
                ]
            ),
        ]
        constraints = [
            CheckConstraint(
                check=Q(end__gt=F("start")),
                name="end_after_start",
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
