from django.contrib import admin

# Register your models here.
# api/admin.py
from django.contrib import admin
from .models import Job, Coordinate, Order  # Import your models

# Register your models
admin.site.register(Job)
admin.site.register(Coordinate)
admin.site.register(Order)