from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from studentSchema import Student
from django.db import connection
from django.contrib.auth import authenticate, login


class LoginStudent(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        return render(request, 'LogIn.html')
    

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success' : True, 'message' : f'Successfully logged in {email}'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid username or password, please try again.'})
        

class RegisterStudent(View):
    def get(self, request):
        return render(request, 'register.html')
    

    def post(self, request):
        name_first = request.POST.get('name_first')
        name_last = request.POST.get('name_last')
        name_middle = request.POST.get('name_middle', '')
        email = request.POST.get('email')
        password = request.POST('password')

        if name_first and name_last and email and password:
            student = Student(name_first = name_first, name_last = name_last, name_middle = name_middle, email = email, student_password = password)

            student.save()

            return JsonResponse({'success' : True, 'message' : f'Successfully registered {name_last}, {name_first}'})
        else:
            return JsonResponse({'success' : False, 'message' : 'Missing required fields'})