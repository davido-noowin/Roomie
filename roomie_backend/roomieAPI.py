from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from roomSchema import Room

class RoomieAPI(View):
    def get(self, request):
        rooms = Room.objects.all()

        room_names = [room.room_id for room in rooms]

        response = ', '.join(room_names)
        return HttpResponse(response)
    

    def post(self, request):
        return HttpResponse('post resonse handled')