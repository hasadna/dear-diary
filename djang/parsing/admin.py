from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Calendar)
admin.site.register(models.Event)


class DownloadReportAdmin(admin.ModelAdmin):
    list_filter = ("resource_id", "status")


admin.site.register(models.DownloadReport, DownloadReportAdmin)
