from django.db import models

class Student(models.Model):
    name_first = models.CharField(max_length = 50)
    name_last = models.CharField(max_length = 50)
    name_middle = models.CharField(max_length = 50, default = '')
    email = models.EmailField(primary_key=True)
    student_password = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'roomie_backend'
        db_table = 'Student'