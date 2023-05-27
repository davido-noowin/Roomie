from django.db import models

class Room(models.Model):
    room_id = models.CharField(max_length=20, primary_key=True)
    location = models.CharField(max_length=50)
    room_size = models.IntegerField()
    room_number = models.IntegerField()

    class Meta:
        app_label = 'roomie_backend'
        db_table = 'Room'