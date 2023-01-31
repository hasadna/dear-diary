from django.db import models
from django.utils import timezone

# website:
# unprocessed file
# processed file

class FileImportResult(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    resource_id = models.UUIDField(db_index=True, unique=True)
    result_is_successful = models.BooleanField()
    result_error = models.TextField(null=True)

class UnprocessedFile(models.Model):
    resource_id = models.UUIDField(db_index=True, unique=True)
    mime_type = models.CharField(max_length=100)
    name = models.CharField(max_length=99)
    url = models.CharField(max_length=300)
