from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Roomaccomodations
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


def account(response:HttpResponse) -> HttpResponse:
    return render(response, 'main/account.html', {})


def createAccount(response:HttpResponse) -> HttpResponse:
    form = NewUserForm()

    if response.method == 'POST':
        form = NewUserForm(response.POST)
        if form.is_valid():
            form.save()
    
    context = {
        'form' : form
    }

    return render(response, 'main/register.html', context)
