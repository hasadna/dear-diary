"""djang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from parsing.views import (
    calendar_list,
    events_feed,
    HomePageView,
    DownloadReportListView,
    DownloadReportDetailView,
    CalendarDetailView,
    AboutView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutView.as_view()),
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("api/calendars/", calendar_list),
    path("api/events/<int:calendar_id>", events_feed),
    path(
        "download_reports/",
        DownloadReportListView.as_view(),
        name="download-reports-list",
    ),
    path(
        "download_reports/<pk>",
        DownloadReportDetailView.as_view(),
        name="download-reports-detail",
    ),
    path(
        "calendars/<pk>",
        CalendarDetailView.as_view(),
        name="calendar-view",
    ),
]
