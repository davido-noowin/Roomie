from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def home(response:HttpResponse) -> HttpResponse:
    return render(response, 'main/home.html')
