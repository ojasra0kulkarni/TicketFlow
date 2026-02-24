from django.shortcuts import render
from django.http import HttpRequest
from .models import Ticket
from .analytics import get_ticket_analytics
from .analytics_utils import generate_priority_dashboard
from django.db.models import Q
from datetime import datetime

def analytics_dashboard(request):
    tickets = Ticket.objects.all()
    city = request.GET.get("city")
    priority = request.GET.get("priority")
    status = request.GET.get("status")
    if city:
        tickets = tickets.filter(address=city)

    if priority:
        tickets = tickets.filter(priority=priority)

    if status:
        tickets = tickets.filter(status=status)

    analytics_data = get_ticket_analytics(tickets)
    priority_data = generate_priority_dashboard(tickets)

    data = {**analytics_data, **priority_data}

    data["cities"] = Ticket.objects.values_list("address", flat=True).distinct()
    data["priorities"] = Ticket.objects.values_list("priority", flat=True).distinct()
    data["statuses"] = Ticket.objects.values_list("status", flat=True).distinct()

    return render(request, "ticketflowapp/analysis.html", data)

def loadHome(request):
    return render(request, "ticketflowapp/home.html")