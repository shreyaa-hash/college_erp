from django.contrib import admin
from .models import Student, Attendance, Notice,Timetable,Marks,Faculty     

admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Notice)
admin.site.register(Timetable)
admin.site.register(Marks)
admin.site.register(Faculty)