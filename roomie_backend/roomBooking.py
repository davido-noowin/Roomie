from django.db import models
from studentSchema import Student
from roomSchema import Room

class RoomBooking(models.Model) :
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "room")