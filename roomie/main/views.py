from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Room, RoomAccomodations
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import NewUserForm
from collections import defaultdict
import datetime
import calendar


def home(response:HttpResponse) -> HttpResponse:
    #room_info = Room.objects.all()
    #print(room_info)

    return render(response, 'main/index.html', {})


def reserve(response:HttpResponse, study_room:str='MRC') -> HttpResponse:
    abbreviation_mapping = {
        'MRC' : 'Multimedia Resources Center',
        'Science' : 'Science Library',
        'Langson' : 'Langson Library',
        'Gateway' : 'Gateway Study Center',
    }

    #study_room = 'Langson'
    accomodations = RoomAccomodations.objects.all()
    rooms_list = Room.objects.all().filter(room_id__startswith=study_room)

    # set up the paginator
    pager = Paginator(rooms_list, 4)
    page = response.GET.get('page')
    rooms = pager.get_page(page)

    #for item in accomodations:
    #    print(item.room, item.accomodation)
    #print()
    #for item in rooms:
    #    print(item.room_id, item.room_number, item.room_size, item.location)


    today = datetime.date.today()
    current_year = today.year
    current_month = calendar.month_name[today.month]
    current_day = today.day

    week_window = datetime.date(current_year, today.month, current_day + 7)
    w1 = datetime.date(current_year, today.month, current_day)
    w2 = datetime.date(current_year, today.month, current_day + 1)
    w3 = datetime.date(current_year, today.month, current_day + 2)
    w4 = datetime.date(current_year, today.month, current_day + 3)
    w5 = datetime.date(current_year, today.month, current_day + 4)
    w6 = datetime.date(current_year, today.month, current_day + 5)
    w7 = datetime.date(current_year, today.month, current_day + 6)
    # print(week_window.year, week_window.month, week_window.day)
    
    
    context = {
        'year' : current_year,
        'current_month' : current_month,
        'current_day' : current_day,
        'altered_month' : calendar.month_name[week_window.month],
        'altered_day' : week_window.day,
        'd1' : calendar.day_name[w1.weekday()] + ' ' + '(' + w1.strftime("%m/%d/%y") + ')',
        'd2' : calendar.day_name[w2.weekday()] + ' ' + '(' + w2.strftime("%m/%d/%y") + ')',
        'd3' : calendar.day_name[w3.weekday()] + ' ' + '(' + w3.strftime("%m/%d/%y") + ')',
        'd4' : calendar.day_name[w4.weekday()] + ' ' + '(' + w4.strftime("%m/%d/%y") + ')',
        'd5' : calendar.day_name[w5.weekday()] + ' ' + '(' + w5.strftime("%m/%d/%y") + ')',
        'd6' : calendar.day_name[w6.weekday()] + ' ' + '(' + w6.strftime("%m/%d/%y") + ')',
        'd7' : calendar.day_name[w7.weekday()] + ' ' + '(' + w7.strftime("%m/%d/%y") + ')',
        'd8' : calendar.day_name[week_window.weekday()] + ' ' + '(' + week_window.strftime("%m/%d/%y") + ')',
        'rooms' : rooms,
        'result_count' : rooms_list.count(),
        'center' : abbreviation_mapping[study_room]
    }

    return render(response, 'main/reserve1.html', context)


@login_required(login_url='account')
def myrooms(response:HttpResponse, user:str) -> HttpResponse:
    if response.user.email != user:
        return redirect('home')
    
    today = datetime.date.today()
    current_year = today.year
    current_month = calendar.month_name[today.month]
    current_day = today.day

    cal = calendar.Calendar()
    formatted = cal.monthdayscalendar(current_year, today.month)
    days_in_month = defaultdict(list)

    for weeks in formatted:
        for i in range(len(weeks)):
            if weeks[i] == 0:
                 days_in_month[i].append('')
            else:
                days_in_month[i].append(weeks[i])

    print(days_in_month)

    context = {
        'year' : current_year,
        'month' : current_month,
        'day' : current_day,
        'calendar' : formatted,
        'mon' : days_in_month[0],
        'tue' : days_in_month[1],
        'wed' : days_in_month[2],
        'thu' : days_in_month[3],
        'fri' : days_in_month[4],
        'sat' : days_in_month[5],
        'sun' : days_in_month[6],
    }

    return render(response, 'main/my-rooms.html', context)


def about(response:HttpResponse) -> HttpResponse:
    return render(response, 'main/about.html', {})


def bookSuccess(response:HttpResponse) -> HttpResponse:
    context = {}
    return render(response, 'main/book-success.html', context)


@login_required(login_url='account')
def loginSuccess(response:HttpResponse) -> HttpResponse:
    context = {}
    return render(response, 'main/login-success.html', context)


@login_required(login_url='account')
def logoutSuccess(response:HttpResponse) -> HttpResponse:
    logout(response)
    context = {}
    return render(response, 'main/logout.html', context)


def account(response:HttpResponse) -> HttpResponse:
    if response.user.is_authenticated:
        return redirect('home')

    message = 'Login or register to reserve'
    if response.method == 'POST':
        username = response.POST.get('username')
        # print(username)
        password = response.POST.get('password')
        # print(password)

        user = authenticate(response, username=username, password=password)

        if user is not None:
            login(response, user)
            return redirect(loginSuccess)
        else:
            message = 'Email or Password is incorrect'
            print('wrong login')

    return render(response, 'main/account.html', {'message' : message})


def createAccount(response:HttpResponse) -> HttpResponse:
    if response.user.is_authenticated:
        return redirect('home')

    form = NewUserForm()
    message = 'Register for a Roomie account'

    if response.method == 'POST':
        form = NewUserForm(response.POST)
        if form.is_valid():
            inital = form.save(commit=False)
            inital.username = form.cleaned_data['email']
            inital.save()
            login(response, inital)
            return redirect('home')
        else:
            message = 'Email or password not valid'
    context = {
        'form' : form,
        'message' : message
    }

    return render(response, 'main/register.html', context)
