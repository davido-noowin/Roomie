from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def home(response:HttpResponse) -> HttpResponse:
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
    return render(response, 'main/register.html')
