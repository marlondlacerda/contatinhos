from datetime import datetime
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Categoy(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = PhoneNumberField(region="BR")
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Categoy, on_delete=models.CASCADE)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name
