from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpRequest
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Room, RoomsBooked
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import NewUserForm
from collections import defaultdict
import datetime
import calendar

# CONST GLOBALS
OPERATING_TIMES = {
    'MRC' : {
        '6' : [],
        '0' : [13, 14, 15, 16],
        '1' : [13, 14, 15, 16],
        '2' : [13, 14, 15, 16],
        '3' : [13, 14, 15, 16],
        '4' : [13, 14, 15, 16],
        '5' : [],
    },
    'Gateway' : {
        '6' : [17, 18, 19, 20, 21, 22, 23, 0, 1, 2],
        '0' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0, 1, 2],
        '1' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0, 1, 2],
        '2' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0, 1, 2],
        '3' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0, 1, 2],
        '4' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        '5' : [17, 18, 19, 20],
    },
    'Langson' : {
        '6' : [13, 14, 15, 16],
        '0' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
        '1' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
        '2' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
        '3' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
        '4i' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
        '5' : [13, 14, 15, 16, 17, 18, 19, 20],
    },
    'Science' : {
        '6' : [13, 14, 15, 16],
        '0' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
        '1' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
        '2' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
        '3' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
        '4' : [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
        '5' : [13, 14, 15, 16],
    }
}


# Helper Functions
def parseTime(parsing:str) -> int:
    try:
        time = parsing.split(' - ')[1]
        if 'PM' in time:
            hour = int(time.split(' PM')[0])
            if hour != 12:
                hour += 12

                return hour
        else:
            hour = int(time.split(' AM')[0])
            if hour == 12:
                hour += 12
            
            return hour
    except IndexError:
        return 0
    


def home(response:HttpResponse) -> HttpResponse:
    #room_info = Room.objects.all()
    #print(room_info)

    return render(response, 'main/index.html', {})


def reserve(response:HttpRequest, study_room:str= '') -> HttpResponse:
    abbreviation_mapping = {
        'MRC' : 'Multimedia Resources Center',
        'Science' : 'Science Library',
        'Langson' : 'Langson Library',
        'Gateway' : 'Gateway Study Center',
        '' : 'All Centers'
    }

    rooms_list = Room.objects.all().order_by('room_id')

    if response.GET.get('study-room') is not None:
        study_room = response.GET.get('study-room')
        rooms_list = rooms_list.filter(location=abbreviation_mapping[study_room])

    if response.method == 'POST':
        for key, value in response.POST.items():
            if key != 'csrfmiddlewaretoken' and key != 'filter-room-size' and key not in abbreviation_mapping:
                rooms_list = rooms_list.filter(roomaccomodations__accomodation=value.lower())

            if key == 'filter-room-size':
                rooms_list = rooms_list.filter(Q(room_size__gte=int(value)))

            if key in abbreviation_mapping:
                rooms_list = rooms_list.filter(location__exact=value)
                


    # set up the paginator
    pager = Paginator(rooms_list, 4)
    page = response.GET.get('page')
    rooms = pager.get_page(page)


    #for item in accomodations:
    #    print(item.room, item.accomodation, item.room.room_id)
    #print()
    #for item in rooms:
    #    print(item.room_id, item.room_number, item.room_size, item.location)


    today = datetime.date.today()
    current_year = today.year
    current_month = calendar.month_name[today.month]
    current_day = today.day
    new_day_counter = 1

    date_storage = []
    for day in range(8):
        try:
            date_storage.append(datetime.date(current_year, today.month, current_day + day))
        except ValueError:
            date_storage.append(datetime.date(current_year, today.month+1, new_day_counter))
            new_day_counter += 1               


    week_window = date_storage[7]
    w1 = date_storage[0]
    w2 = date_storage[1]
    w3 = date_storage[2]
    w4 = date_storage[3]
    w5 = date_storage[4]
    w6 = date_storage[5]
    w7 = date_storage[6]
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
        'center' : abbreviation_mapping[study_room],
    }

    return render(response, 'main/reserve1.html', context)


@login_required(login_url='account')
def confirmReservation(response:HttpResponse):
    # message is used to 
    message = 'Finalize your reservation'

    today = datetime.date.today()
    weekday = today.weekday()

    start_date = today
    end_date = start_date + datetime.timedelta(days=7)

    next_week_dates = []
    current_date = start_date

    while current_date <= end_date:
        next_week_dates.append(current_date)
        current_date += datetime.timedelta(days=1)


    studyroom_selection_window = [
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ]
    for d in next_week_dates:
        studyroom_selection_window[d.weekday()].append(d.day)
        if d.weekday() != weekday:
            studyroom_selection_window[d.weekday()].append('')

    # print(studyroom_selection_window)

    current_month = calendar.month_name[next_week_dates[0].month]
    # print(current_month)
    next_week_month = calendar.month_name[next_week_dates[7].month]
    # print(next_week_month)

    header = ''
    if current_month != next_week_month and next_week_dates[0].year != next_week_dates[7].year:
        header = f'{current_month} {next_week_dates[0].year} - {next_week_month} {next_week_dates[7].year}'
    elif current_month != next_week_month:
        header = f'{current_month} - {next_week_month} {next_week_dates[7].year}'
    else:
        header = f'{current_month} - {next_week_dates[7].year}'



    booking_response = response.GET.get('booking')

    try:
        room_booking = Room.objects.get(room_id=booking_response)


        if room_booking.location == 'Multimedia Resources Center':
            working_hours = OPERATING_TIMES['MRC'][str(weekday)]
        elif room_booking.location == 'Langson Library':
            working_hours = OPERATING_TIMES['Langson'][str(weekday)]
        elif room_booking.location == 'Science Library':
            working_hours = OPERATING_TIMES['Science'][str(weekday)]
        elif room_booking.location == 'Gateway Study Center':
            working_hours = OPERATING_TIMES['Gateway'][str(weekday)]
        else:
            print('invalid center selection')
        

        # print(working_hours)

    except Room.DoesNotExist:
        return redirect(reserve)


    availability = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0, 1, 2, 3]
    hours = availability.copy()
    end_hours = [hour + 1 for hour in hours]

    booked_rooms = None
    booked_hours = []
    try:
        booked_rooms = RoomsBooked.objects.all().filter(room=booking_response)

        for booking in booked_rooms:
            if booking.booking_start_date.date() == today:
                starting_time = booking.booking_start_date.hour
                ending_time = booking.booking_end_date.hour
                while starting_time <= ending_time:
                    booked_hours.append(starting_time)
                    starting_time += 1

    except RoomsBooked.DoesNotExist:
        pass


    for hour in availability:
        if hour in booked_hours:
            availability[availability.index(hour)] = 'Booked'
        elif hour not in working_hours:
            availability[availability.index(hour)] = 'Unavailable'
        else:
            availability[availability.index(hour)] = 'OPEN'

    
    start_time_display = []
    for i in range(len(hours)):
        if availability[i] == 'OPEN':
            if hours[i] == 0:
                start_time_display.append(f'{room_booking.location} {room_booking.room_number} - 12 AM')
            elif hours[i] > 12:
                start_time_display.append(f'{room_booking.location} {room_booking.room_number} - {hours[i] - 12} PM')
            elif hours[i] == 12:
                start_time_display.append(f'{room_booking.location} {room_booking.room_number} - 12 PM')
            else:
                start_time_display.append(f'{room_booking.location} {room_booking.room_number} - {hours[i]} AM')

    start_selection = None
    if response.GET.get('start') is not None:
        start_selection = response.GET.get('start')
        # print(start_selection)
        
    end_selection = None
    time1 = -1
    time2 = -1

    if response.GET.get('end') is not None:
        end_selection = response.GET.get('end')

        time1 = parseTime(start_selection)
            
        time2 = parseTime(end_selection)

    # Doing checks to confirm correct study room selection and making the reservation
    if response.method == 'POST':
        if (time1 == 24):
            # convert 12am (24) to 0 so that the math works out
            time1 = 0
        diff = time2 - time1

        if start_selection is None:
            message = 'Select a start time'
        elif end_selection is None:
            message = 'Select an end time'
        elif diff < 1 or diff > 2:
            message = 'Invalid start and end times'
        elif time1 in booked_hours:
            message = 'Room has been booked during that time'
        else:
            pass
            begin = timezone.make_aware(datetime.datetime.combine(today, datetime.time(time1, 0)))
            end = timezone.make_aware(datetime.datetime.combine(today, datetime.time(time2, 0)))
            booking = RoomsBooked(room=room_booking, user=response.user, booking_start_date=begin, booking_end_date=end)
            booking.save()
            return render(response, 'main/book-success.html', {})


    end_time_display = []
    for i in range(len(end_hours)):
        if availability[i] == 'OPEN':
            if hours[i] == 24:
                end_time_display.append(f'{room_booking.location} {room_booking.room_number} - 12 AM')
            elif end_hours[i] > 12:
                end_time_display.append(f'{room_booking.location} {room_booking.room_number} - {end_hours[i] - 12} PM')
            elif end_hours[i] == 12:
                end_time_display.append(f'{room_booking.location} {room_booking.room_number} - 12 PM')
            else:
                end_time_display.append(f'{room_booking.location} {room_booking.room_number} - {end_hours[i]} AM')
    

    context = {
        'message' : message,
        'room' : room_booking,
        'header' : header,
        'mon' : studyroom_selection_window[0],
        'tue' : studyroom_selection_window[1],
        'wed' : studyroom_selection_window[2],
        'thu' : studyroom_selection_window[3],
        'fri' : studyroom_selection_window[4],
        'sat' : studyroom_selection_window[5],
        'sun' : studyroom_selection_window[6],
        'open_room' : start_time_display,
        'ending_room' : end_time_display,
        'ava' : availability[0],
        'avb' : availability[1],
        'avc' : availability[2],
        'avd' : availability[3],
        'ave' : availability[4],
        'avf' : availability[5],
        'avg' : availability[6],
        'avh' : availability[7],
        'avi' : availability[8],
        'avj' : availability[9],
        'avk' : availability[10],
        'avl' : availability[11],
        'avm' : availability[12],
        'avn' : availability[13],
        'avo' : availability[14],
        'avp' : availability[15],
        'avq' : availability[16],
        'avr' : availability[17],
        'avs' : availability[18],
        'avt' : availability[19],
        'start' : start_selection,
        'end' : end_selection
    }
    return render(response, 'main/reserve2.html', context)


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

    # print(days_in_month)

    # Getting booking information
    booked_rooms = RoomsBooked.objects.all().filter(user=response.user)
    booked_rooms = sorted(list(booked_rooms), key= lambda room : room.booking_start_date)
    booking = booked_rooms.copy()
    for room in booked_rooms:
        if room.booking_start_date.date() != today:
            booking.remove(room)

    # print(booked_rooms)

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
        'rooms' : booking
    }

    return render(response, 'main/my-rooms.html', context)


def about(response:HttpResponse) -> HttpResponse:
    return render(response, 'main/about.html', {})


@login_required(login_url='account')
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
