from django.shortcuts import render
from django.http import JsonResponse

from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView


from parsing.models import Calendar, Event, DownloadReport
from datetime import datetime, timezone

from .forms import DownloadReportSearchForm


def calendar_list(request):
    cals = Calendar.objects.exclude(event=None).order_by(
        "-when_created_at_source", "pk"
    )
    ret = [cal.to_dict() for cal in cals]
    return JsonResponse({"calendars": ret})


def parse_date(s):
    return datetime.fromisoformat(s)


def events_feed(request, calendar_id):
    start_str = request.GET.get("start")
    start = parse_date(start_str)
    end_str = request.GET.get("end")
    end = parse_date(end_str)
    events = Event.objects.filter(
        calendar__id=calendar_id,
        start__range=(start, end),
    )
    ret = [event.to_dict() for event in events]
    return JsonResponse(ret, safe=False)


class HomePageView(TemplateView):
    template_name = "home.html"

class AboutView(TemplateView):
    template_name = "about.html"

class DownloadReportListView(ListView):
    model = DownloadReport

    def get_context_data(self, **kwargs):
        kwargs["search_form"] = DownloadReportSearchForm()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        qs = DownloadReport.objects.all()
        form = DownloadReportSearchForm(self.request.GET)
        if form.is_valid():
            if resource_id := form.cleaned_data["resource_id"]:
                qs = qs.filter(resource_id=resource_id)

            if status := form.cleaned_data["status"]:
                qs = qs.filter(status=status)

        return qs


class DownloadReportDetailView(DetailView):
    model = DownloadReport

class CalendarDetailView(DetailView):
    model = Calendar

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        calendar = ret['calendar']
        ret['start_url'] = calendar.get_calendar_url(calendar.get_start())
        ret['end_url'] = calendar.get_calendar_url(calendar.get_end())
        return ret
