from webbrowser import register
from django.contrib.auth.models import Permission
from django.contrib import admin
from user.models import Student, Teacher, Staff, Adminn, Booking, Booking_student, Booking_teacher, Booking_staff, Booking_list, Room, Room_type
# Register your models here.
admin.site.register(Student)

admin.site.register(Teacher)

admin.site.register(Staff)

admin.site.register(Adminn)

admin.site.register(Booking)

admin.site.register(Booking_student)

admin.site.register(Booking_teacher)

admin.site.register(Booking_staff)

admin.site.register(Booking_list)

admin.site.register(Room)

admin.site.register(Room_type)


# admin.site.register(Permission)