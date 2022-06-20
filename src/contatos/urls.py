from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="contact_list"),
    path('search/', views.search, name='search'),
    path(
        "contacts/<int:contact_id>",
        views.list_contact,
        name="contact_details",
        ),
    path("contacts/new/", views.new_contact, name="new_contact"),
    path(
        "contacts/<int:contact_id>/edit/",
        views.edit_contact,
        name="new_contact",
        ),
    path(
        "contacts/<int:contact_id>/delete/",
        views.delete_contact,
        name="delete_contact",
        ),
]
