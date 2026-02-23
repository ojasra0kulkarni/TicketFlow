from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password
import re

def home(request):
    if not request.session.get('user_id'):
        return redirect("login")
    return render(request, "home.html")

def register(request):
  if request.method =="POST":
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")

    # check if the password matches
    if password != confirm_password:
      return render(request, "accounts/register.html",{
        "error": "password do not match"
      })
    

    #Username must be unique
    if User.objects.filter(username = username).exists():
      return render(request,"accounts/register.html",{
        "error": "Username already exists"
      })
    
    #Username validation
    
    if not re.search(r'[a-z]', username):
      return render(request,"accounts/register.hmtl",{
        "error": "Username must contain at least one lowercase letter"
      })
    if not re.search(r'[A-Z]', username):
      return render(request,"accounts/register.html",{
        "error": "Username must contain at least one uppercase letter"
      })
    if not re.search(r'[@#$%*_&]',username):
      return render(request, "accounts/register.html",{
        "error": "Username must contain at least one special charcter"
      })
    
    #Password Strength check

    if len(password) < 6:
      return render(request, "accounts/register.html", {
        "error": "Password must be at least 6 characters long"
      })
    
    #Strong Password rule

    if not re.search(r'[A-Z]', password) or \
       not re.search(r'[a-z]', password) or \
       not re.search(r'[0-9]', password) or \
       not re.search(r'[@#$%&*_]', password):
        return render(request, "accounts/register.html", {
          "error": "password must contain uppercase, lowercase, number and special character"
        })
    hashed_password = make_password(password)
    User.objects.create(username=username,
                        email=email,
                        password = hashed_password
                        )
      
    return redirect("login")
  return render(request, "accounts/register.html")



def login(request):
  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")

    try:
      user = User.objects.get(username = username)
    except User.DoesNotExist:
      return render(request, "accounts/login.html", {
        "error": "Invalid credentials"
      })
    if check_password(password, user.password):
      request.session['user_id'] = user.id
      request.session['username'] = user.username
      return redirect("LoadHome")
    else:
      return render(request, "accounts/login.html", {
        "error": "Invalid credentials"
      })
  return render(request, "accounts/login.html")

      



