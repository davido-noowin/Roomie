from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("reserve/", views.reserve, name="reserve"),
    path("my-rooms/<str:user>/", views.myrooms, name="my-rooms"),
    path("about/", views.about, name="about"),
    path("account/", views.account, name="account"),
    path("register/", views.createAccount, name="register"),
    path("book-success/", views.bookSuccess, name="book-success"),
    path("login-success/", views.loginSuccess, name="login-success"),
    path("logout/", views.logoutSuccess, name="logout"),
    path("confirm-reservation/", views.confirmReservation, name="confirmation"),
]