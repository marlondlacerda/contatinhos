from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('search/', views.search, name='search'),
    path("contacts/<int:contact_id>", views.list_contact, name="list_contact"),
    path("contacts/new/", views.new_contact, name="new_contact"),
]
