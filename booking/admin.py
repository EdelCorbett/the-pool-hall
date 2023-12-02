from django.contrib import admin
from .models import CustomUser, Table, Bookings, TimeSlots
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Table)
admin.site.register(Bookings)
admin.site.register(TimeSlots)