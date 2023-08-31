from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User


class Student(models.Model):
    name_first = models.CharField(max_length=50, blank=True, null=True)
    name_last = models.CharField(max_length=50, blank=True, null=True)
    name_middle = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'student'


class Room(models.Model):
    room_id = models.CharField(primary_key=True, max_length=20)
    location = models.CharField(max_length=50)
    room_size = models.IntegerField(blank=True, null=True)
    room_number = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=100, null=True)
    room_desc = models.CharField(max_length=999, null=True)

    class Meta:
        managed = False
        db_table = 'room'


class RoomsBooked(models.Model):
    booking_number = models.IntegerField(primary_key=True, null=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_start_date = models.DateTimeField(null=True)
    booking_end_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'roomsbooked'

    def save(self, *args, **kwargs):
        if not self.booking_number:  # If booking_number is not provided
            # Get the maximum booking_number currently in the database
            max_booking_number = RoomsBooked.objects.aggregate(Max('booking_number'))['booking_number__max']
            if max_booking_number is None:
                max_booking_number = 0
            self.booking_number = max_booking_number + 1
        
        super(RoomsBooked, self).save(*args, **kwargs)
        



class RoomAccomodations(models.Model):
    room = models.OneToOneField(Room, models.DO_NOTHING, primary_key=True)  # The composite primary key (room_id, accomodation) found, that is not supported. The first column is selected.
    accomodation = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'roomaccomodations'
        unique_together = (('room', 'accomodation'),)
