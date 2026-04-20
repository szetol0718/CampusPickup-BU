# File: admin.py
# Author: Louis Szeto (szetol@bu.edu), 20/4/2026
# Description: Register campus pickup models with the Django admin site.

from django.contrib import admin
from .models import Profile, Ride, RideParticipant, RideMessage

admin.site.register(Profile)
admin.site.register(Ride)
admin.site.register(RideParticipant)
admin.site.register(RideMessage)