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
    image = models.ImageField(
        upload_to="pictures/%Y/%m/",
        blank=True,
        null=True
    )
    phone = PhoneNumberField(region="BR")
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Categoy, on_delete=models.CASCADE)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return f"{self.name} {self.get_last_name()}"

    def get_last_name(self):
        if self.last_name:
            return self.last_name
        else:
            return ""

    def get_email(self):
        if self.email:
            return self.email
        else:
            return "Não informado"
