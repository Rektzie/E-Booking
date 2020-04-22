from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.forms import ModelForm
# Create your models here.


class Student(models.Model):
    mj = (
    (1, "it"),
    (2, "dsba"),
    (3, "bit"),
    )
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    stu_id = models.IntegerField()
    year = models.IntegerField()
    major = models.IntegerField(choices=mj)




class Adminn(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
  

class Teacher(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.CharField(max_length=255)

class Staff(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)

class Booking(models.Model):
    st = (
    (1, "รอการอนุมัติ"),
    (2, "อนุมัติ"),
    (3, "ไม่อนุมัติ"),
    )
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    date = models.DateTimeField(default=datetime.now, blank=True)
    bookdate = models.DateField()
    status = models.IntegerField(choices=st, default = 1)
    
    status_remark = models.IntegerField(choices=st, default = 1)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Booking_student(models.Model):
    booking_id = models.OneToOneField(Booking, on_delete=models.CASCADE)
    teacher_user_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    staff_user_id = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    teacher_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    teacher_result = models.BooleanField(default=False)
    staff_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    staff_result = models.BooleanField(default=False)

class Booking_teacher(models.Model):
    booking_id = models.OneToOneField(Booking, on_delete=models.CASCADE)

class Booking_staff(models.Model):
    booking_id = models.OneToOneField(Booking, on_delete=models.CASCADE)

class Room_type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.IntegerField()
    room_type = models.ForeignKey(Room_type, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Booking_list(models.Model):
    list_no = models.AutoField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)


class AddRoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'start_time', 'end_time', 'capacity', 'room_type']