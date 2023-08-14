from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("reserve/", views.reserve, name="reserve"),
    path("my-rooms/", views.myrooms, name="my-rooms"),
    path("about/", views.about, name="about"),
    path("account/", views.account, name="account")
]