from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from roomAccomodationsSchema import RoomsAccomodation
from django.db import connection
from collections import defaultdict

class RoomieAPIRoomAccomodations(View):
    def get(self, request):
        '''
        The get method will provide a dictionary of all the accomodations that a study room can provide
        Key: room id
        Value: a list with the accomodations that the room will provide
        '''
        accomodations = RoomsAccomodation.objects.all()

        accomodation_info = defaultdict(list)
        #print(accomodations)
        for element in accomodations:
            print(element.room_id)
            accomodation_info[str(element.room_id)].append(element.accomodation)

        #print(accomodation_info)
        response = accomodation_info
        return HttpResponse(str(accomodation_info))

    def get_table_name(self, model_class):
        table_name = model_class._meta.db_table

        return model_class.room_id