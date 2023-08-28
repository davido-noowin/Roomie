from django.db import models


class Student(models.Model):
    name_first = models.CharField(max_length=50, blank=True, null=True)
    name_last = models.CharField(max_length=50, blank=True, null=True)
    name_middle = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'student'


class RoomsBooked(models.Model):
    email = models.OneToOneField('Student', models.DO_NOTHING, db_column='email', primary_key=True)  # The composite primary key (email, room_booked) found, that is not supported. The first column is selected.
    room_booked = models.CharField(max_length=20)
    date_booked = models.DateTimeField()
    duration_booked = models.IntegerField(blank=True)

    class Meta:
        managed = False
        db_table = 'roomsbooked'
        unique_together = (('email', 'room_booked'),)


class Room(models.Model):
    room_id = models.CharField(primary_key=True, max_length=20)
    location = models.CharField(max_length=50)
    room_size = models.IntegerField(blank=True, null=True)
    room_number = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=100)
    room_desc = models.CharField(max_length=999)

    class Meta:
        managed = False
        db_table = 'room'


class RoomAccomodations(models.Model):
    room = models.OneToOneField(Room, models.DO_NOTHING, primary_key=True)  # The composite primary key (room_id, accomodation) found, that is not supported. The first column is selected.
    accomodation = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'roomaccomodations'
        unique_together = (('room', 'accomodation'),)
