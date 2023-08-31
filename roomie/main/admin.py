from django.contrib import admin
from .models import RoomsBooked

class RoomsBookedAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'room', 'user', 'booking_start_date', 'booking_end_date')

admin.site.register(RoomsBooked, RoomsBookedAdmin)
