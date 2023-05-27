from django.db import models

class Student(models.Model):
    name_first = models.CharField(max_length = 50)
    name_last = models.CharField(max_length = 50)
    name_middle = models.CharField(max_length = 50, default = '')
    email = models.EmailField(primary_key=True)