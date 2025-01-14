from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
import os


class Schedule(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    schedule = models.JSONField(default=dict)
    class_name = models.CharField(max_length=3)
    school_shift = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100)
    region_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.creator}-{self.id}"

