from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    available_space = models.FloatField(default=0)


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    CREATED = 1
    IN_PROGRESS = 50
    COMPLETED = 99
    STATUS_CHOICES = (
        (CREATED, "Created"),
        (IN_PROGRESS, "In progress"),
        (COMPLETED, "Completed"),
    )
    total_space = models.FloatField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=CREATED)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)


class Pull(models.Model):
    STARTED = 1
    COMPLETED = 99
    STATUS_CHOICES = (
        (STARTED, "Started"),
        (COMPLETED, "Completed"),
    )
    total_space = models.FloatField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STARTED)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)


class Container(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, blank=True, null=True)
    pull = models.ForeignKey(Pull, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    location_building = models.CharField(max_length=255)
    location_room = models.CharField(max_length=255)
    location_range = models.CharField(max_length=5)
    location_shelf = models.CharField(max_length=5)
    box_number = models.CharField(max_length=10)
    barcode = models.CharField(max_length=200)
    height = models.FloatField()
    width = models.FloatField()
    depth = models.FloatField()
