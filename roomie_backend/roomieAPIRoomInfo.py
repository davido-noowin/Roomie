from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from roomSchema import Room

class RoomieAPIRoomInfo(View):
    def get(self, request):
        '''
        The get method will provide a dictionary of all the possible study rooms at UCI
        Key: room id
        Value: a list with the following attributes - location, capacity, room_number
        '''
        rooms = Room.objects.all()

        room_info = {room.room_id : [f'Location: {room.location}', f'Capacity: {room.room_size}', f'Room Number: {room.room_number}']for room in rooms}
        #print(room_info)
        response = room_info
        return JsonResponse(response)