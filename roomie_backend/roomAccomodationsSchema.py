from django import models
from roomSchema import Room

class RoomsAccomodation(models.Models) :
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    accomodation = models.CharField(max_length=20)

    class Meta :
        unique_together = ('room', 'accomodation')
        app_label = 'roomie-backend'
        db_table = 'Room'


        