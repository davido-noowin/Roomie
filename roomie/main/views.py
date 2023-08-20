from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Room, Roomaccomodations
from django.contrib import messages
from .forms import NewUserForm

def home(response:HttpResponse) -> HttpResponse:
    #room_info = Room.objects.all()
    #print(room_info)

    return render(response, 'main/index.html', {})


def reserve(response:HttpResponse) -> HttpResponse:
    return render(response, 'main/reserve1.html', {})


@login_required(login_url='account')
def myrooms(response:HttpResponse, user:str) -> HttpResponse:
    if response.user.email != user:
        return redirect('home')
    return render(response, 'main/my-rooms.html', {})


def about(response:HttpResponse) -> HttpResponse:
    return render(response, 'main/about.html', {})


def bookSuccess(response:HttpResponse) -> HttpResponse:
    context = {}
    return render(response, 'main/book-success.html', context)


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
