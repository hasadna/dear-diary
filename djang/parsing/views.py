from django.shortcuts import render
from django.http import JsonResponse

from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView

from parsing.models import Calendar, Event
from datetime import datetime,timezone

def calendar_list(request):
    cals = Calendar.objects.exclude(event=None).all()
    ret = [
        cal.to_dict()
        for cal in cals
    ]
    return JsonResponse({"calendars":ret})

def parse_date(s):
    return datetime.fromisoformat(s)

def events_feed(request, calendar_id):
    start_str = request.GET.get('start')
    start = parse_date(start_str)
    end_str = request.GET.get('end')
    end = parse_date(end_str)
    events = Event.objects.filter(
        calendar__id=calendar_id,
        start__range=(start,end),
    ).all()
    ret = [
        event.to_dict()
        for event in events
    ]
    return JsonResponse(ret, safe=False)


class HomePageView(TemplateView):
    template_name = "home.html"

