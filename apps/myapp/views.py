from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Travel
from datetime import date, datetime
from django.db.models import Count
import bcrypt

def index(request):
    print "This is the index", request
    return render(request, 'myapp/index.html')

def homepage(request):
    print "This is the hompage", request
    isLoggedin = User.objects.get(id=request.session['id'])
    travelz = Travel.objects.all()
    context = {
        "isLoggedin" : isLoggedin,
        "users": User.objects.all(),
        "travels": Travel.objects.all(),
        "mytrips" : Travel.objects.filter(planner__id=request.session['id']),
        "dashtrips": Travel.objects.filter(joiner__id=request.session['id']),
    }
    return render(request, 'myapp/homepage.html', context)

def registration_logic(request):
    print "This is registration", request
    context = {
        "first_name" : request.POST['first_name'],
        "last_name" : request.POST['last_name'],
        "username": request.POST['username'],
        "password" : request.POST['password'],
        "confirm_password" : request.POST['confirm_password']
    }
    flags = User.objects.register(context)
    if flags:
        for flag in flags:
            messages.error(request, flag)
        return redirect('/')
    else:
        pwd = request.POST['password']
        hashed_pw = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], username=request.POST['username'], password=hashed_pw)
        request.session['id'] = user.id
    return redirect('/homepage')

def login_logic(request):
    print "This is the LOGIN LOGIC ****** ", request
    context = {
        "username" : request.POST['username'],
        "password" : request.POST['password']
    }
    flags = User.objects.login(context)
    if flags:
        for flag in flags:
            messages.error(request, flag)
        return redirect('/')
    else:
        logging_user =  User.objects.get(username=request.POST['username'])
        request.session['id'] = logging_user.id
        return redirect('/homepage', context)

def logout(request):
    request.session['id'] = 0
    return redirect('/')

def new_travel(request):
    print "This is the adding travel page"
    return render(request, 'myapp/addtravel.html')

def addtravel(request):
    print "Adding Travel into the database!", request
    context = {
        "destination" : request.POST['destination'],
        "description" : request.POST['description'],
        "start_date" : request.POST['start_date'],
        "end_date" : request.POST['end_date']
    }
    flags = Travel.objects.add_travel(context)
    if flags:
        for flag in flags:
            messages.error(request, flag)
        return redirect('/newtravel')
    else:
        curr_user = User.objects.get(id=request.session['id'])
        new_dest = Travel.objects.create(destination=request.POST['destination'], description=request.POST['description'], trip_start=request.POST['start_date'], trip_end=request.POST['end_date'], planner=curr_user)

    response = "Trip successfully added!"
    return redirect('/homepage')

def travelinfo(request, id):
    print "This is the information about the travel"
    context = {
    }



    return render(request, 'myapp/info.html')
