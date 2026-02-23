from django.shortcuts import render
from django.http import HttpRequest
from .models import Ticket
from .analytics import get_ticket_analytics
from .analytics_utils import generate_priority_dashboard

def analytics_dashboard(request):
    analytics_data = get_ticket_analytics()
    priority_data = generate_priority_dashboard()

    # Merge both dictionaries
    data = {**analytics_data, **priority_data}

    return render(request, "ticketflowapp/analysis.html", data)

def loadHome(request):
    return render(request, "ticketflowapp/home.html")