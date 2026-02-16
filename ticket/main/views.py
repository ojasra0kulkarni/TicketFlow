from django.shortcuts import render
from django.http import HttpResponse
from .models import Data

def home(request):
  d = Data.objects.all()
  return render(request,"dashboard.html",{"D":d})


# Create your views here.
