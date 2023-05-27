from django.db import models
from roomSchema import Room

class RoomsAccomodation(models.Model):
    room_id = models.OneToOneField(Room, db_column = 'room_id', on_delete = models.CASCADE)
    accomodation = models.CharField(max_length=20, primary_key= True)
    

    class Meta :
        #unique_together = ('room_id', 'accomodation')
        app_label = 'roomie_backend'
        db_table = 'RoomAccomodations'