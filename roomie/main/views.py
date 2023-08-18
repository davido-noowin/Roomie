from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Roomaccomodations
from django.contrib import messages
from .forms import NewUserForm

def home(response:HttpResponse) -> HttpResponse:
    #room_info = Room.objects.all()
    #print(room_info)

    return render(response, 'main/index.html', {})


def reserve(response:HttpResponse) -> HttpResponse:
    return render(response, 'main/reserve1.html', {})


def myrooms(response:HttpResponse) -> HttpResponse:
    return render(response, 'main/my-rooms.html', {})


def about(response:HttpResponse) -> HttpResponse:
    return render(response, 'main/about.html', {})


def bookSuccess(response:HttpResponse) -> HttpResponse:
    context = {}
    return render(response, 'main/book-success.html', context)


def loginSuccess(response:HttpResponse) -> HttpResponse:
    context = {}
    return render(response, 'main/login-success.html', context)


def logoutSuccess(response:HttpResponse) -> HttpResponse:
    logout(response)
    context = {}
    return render(response, 'main/logout.html', context)


def account(response:HttpResponse) -> HttpResponse:
    if response.method == 'POST':
        username = response.POST.get('username')
        print(username)
        password = response.POST.get('password')
        print(password)

        user = authenticate(response, username=username, password=password)

        if user is not None:
            login(response, user)
            return redirect(loginSuccess) # TODO: change this to a confirmation page that you logged in
        else:
            messages.info(response, 'Email or Password is incorrect') # FIX
            print('wrong login') # TODO: change this to a page that tells you that you got your login info wrong

    return render(response, 'main/account.html', {})


def createAccount(response:HttpResponse) -> HttpResponse:
    form = NewUserForm()

    if response.method == 'POST':
        form = NewUserForm(response.POST)
        if form.is_valid():
            inital = form.save(commit=False)
            inital.username = form.cleaned_data['email']
            inital.save()
            login(response, inital)
            return redirect('home') # TODO: change this to a confirmation page that you registered
        else:
            return redirect('register') # TODO: change this to a confirmation page that you did not fill in info correctly
    context = {
        'form' : form
    }

    return render(response, 'main/register.html', context)
