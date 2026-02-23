from django.urls import path, include
from . import views

urlpatterns = [
    path('home',views.loadHome,name="LoadHome"),
    path("analytics/", views.analytics_dashboard, name="analytics"),
    
]
