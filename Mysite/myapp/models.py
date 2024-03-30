# registration/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # if the model is deleted the profile should also deleted
    Roll = models.CharField(max_length=100, unique=True)
    call = models.CharField(max_length=15, default="1234567890")

    def __str__(self):
        return self.user.username


class AddQuery(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    # Fields for name, registration number, and phone number
    name = models.CharField(max_length=100, unique=True)
    registration_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)

    # Checkbox field
    checkbox_field = models.BooleanField(default=False)

    # Radio button field with choices
    RADIO_CHOICES = (
        ("PhonePay to Cash", "PhonePay to Cash"),
        ("Cash to Phonepay", "Cash to Phonepay"),
    )
    radio_field = models.CharField(max_length=100, choices=RADIO_CHOICES)

    def __str__(self):
        return self.seller.username


class queryNotification(models.Model):
    owner_name = models.CharField(max_length=100)
    query_creator_name = models.CharField(max_length=100)
    query_name = models.CharField(max_length=100)
    owner_PhNo = models.CharField(max_length=100, blank=True)
    Owner_reg = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.query_creator_name
