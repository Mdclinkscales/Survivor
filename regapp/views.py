from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def home(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.validator(request.POST)
    password = request.POST['password']
    hashpass = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        User.objects.create(firstname=request.POST['firstname'], lastname = request.POST['lastname'], email = request.POST['email'], password = hashpass)
        logged_user = User.objects.last()
        request.session['user'] = User.objects.last()
        request.session['userid'] = logged_user.id
        return redirect('/wall')

def login(request):
    errors = User.objects.loginvalidator(request.POST)
    user = User.objects.filter(email=request.POST['useremail'])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['userpass'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/wall')
    return redirect('/')
def success(request):
    user = request.session['userid']
    context = {
        "user": User.objects.get(id=user)
    }
    return render(request, 'loggedin.html', context)

def logout(request):
    del request.session['userid']
    return redirect('/')