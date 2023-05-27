from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
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
            string_element = str(element.room_id)
            if string_element.startswith('Room object (') and string_element.endswith(')'):
                string_element = string_element[len('Room object ('):-1]
            accomodation_info[string_element].append(element.accomodation)

        #print(accomodation_info)
        response = accomodation_info
        return JsonResponse(accomodation_info)

    def get_table_name(self, model_class):
        table_name = model_class._meta.db_table

        return model_class.room_id