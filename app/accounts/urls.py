from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="index_login"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
]
