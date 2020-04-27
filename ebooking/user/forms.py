from builtins import object
from tkinter import Widget

from django import forms
from user.models import Room_type, Booking_list
from user.models import Room
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, timedelta


class EditForm(forms.Form):
    name = forms.CharField(max_length=255)
    date = forms.DateField()
    
    
class TimeInput(forms.TimeInput):
    input_type = 'time'    
    
class DateInput(forms.DateInput):
    input_type = 'date' 
    
class AddRoomForm(forms.Form): #form add, book
    roomType = Room_type.objects.all()
    roomTypeChoices = [('', 'select')]
    for i in roomType:
        roomTypeChoices.append((i.id, i.name))
        
    name = forms.CharField(label='ชื่อห้อง' ,max_length=30, required=True)

    start_time = forms.TimeField(label='เวลาเปิด' ,widget=TimeInput, required=True)
    end_time = forms.TimeField(label='เวลาปิด' ,widget=TimeInput, required=True)
    capacity = forms.IntegerField(label='ความจุห้อง' ,required=True)
    room_type = forms.ChoiceField(label='ประเภทห้อง' ,widget=forms.Select, choices=roomTypeChoices)

    name.widget.attrs.update({'class' : 'form-control'})
    room_type.widget.attrs.update({'class' : 'form-control'})
    start_time.widget.attrs.update({'class' : 'form-control'})
    end_time.widget.attrs.update({'class' : 'form-control'})
    capacity.widget.attrs.update({'class' : 'form-control'})
    
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        
        try:
            room = Room.objects.get(name=name)
            # room = Room.objects.get(name=request.POST.get('name'))

        except ObjectDoesNotExist:
            room = None

        if room:
            # raise ValidationError(
            #     'ห้องชื่อ %(name)s มีอยู่ในระบบแล้ว', code='invalid', params={'roomName' : name}
            errorMsg = 'ห้องชื่อนี้มีอยู่ในระบบแล้ว'
            self.add_error('name', errorMsg)
            # )

class BookRoomDescriptionForm(forms.Form):
    description = forms.CharField(label='เหตุผลในการจอง', widget=forms.Textarea, required=True)
    def clean(self):
        cleaned_data = super().clean()
        
    description.widget.attrs.update({'class' : 'form-control'})
                
            
class BookRoomForm(forms.Form): #for booking_list
    
    bookdate = forms.DateField(label='วันที่', widget=DateInput, required=True)
    start_time = forms.TimeField(label='จองเวลา' ,widget=TimeInput, required=True)
    end_time = forms.TimeField(label='ถึงเวลา' ,widget=TimeInput, required=True)
    
    
    bookdate.widget.attrs.update({'class' : 'form-control', 'max':'3000-12-31'})
    start_time.widget.attrs.update({'class' : 'form-control'})
    end_time.widget.attrs.update({'class' : 'form-control'})
    

    def clean(self):
        cleaned_data = super().clean()
        allBookingList = Booking_list.objects.all()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        bookdate = cleaned_data.get('bookdate')
        
        for each in allBookingList:
            if ((start_time >= each.start_time and start_time <= each.end_time) or 
                (end_time >= each.start_time and end_time <= each.end_time)) and each.bookdate == bookdate:
                errorMsg = 'จองเวลาซ้ำ'
                self.add_error('bookdate', errorMsg)
                print('จองเวลาซ้ำ')
            
class RangeBookingForm(forms.Form):
    fromDate = forms.DateField(label='ตั้งแต่', widget=DateInput, required=True)
    toDate = forms.DateField(label='จนถึง', widget=DateInput, required=True)
    fromTime = forms.TimeField(label='จองเวลา' ,widget=TimeInput, required=True)
    toTime = forms.TimeField(label='ถึงเวลา' ,widget=TimeInput, required=True)
    description = forms.CharField(label='เหตุผลในการจอง', widget=forms.Textarea, required=True)
    
    fromDate.widget.attrs.update({'class' : 'form-control', 'max':'3000-12-31'})
    toDate.widget.attrs.update({'class' : 'form-control', 'max':'3000-12-31'})
    fromTime.widget.attrs.update({'class' : 'form-control'})
    toTime.widget.attrs.update({'class' : 'form-control'})
    description.widget.attrs.update({'class' : 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        allBookingList = Booking_list.objects.all()
        fromDate = cleaned_data.get('fromDate')
        toDate = cleaned_data.get('toDate')
        fromTime = cleaned_data.get('fromTime')
        toTime = cleaned_data.get('toTime')
        state = 1
        
        if fromDate > toDate:
            errorMsg = 'วันที่ไม่ถูกต้อง'
            self.add_error('fromDate', errorMsg)
            print('date-error')
        if fromTime > toTime:
            errorMsg = 'เวลาไม่ถูกต้อง'
            self.add_error('fromTime', errorMsg)
            print('Time-error')  
            
                 
        delta = toDate - fromDate # as timedelta
  
        for i in range(delta.days + 1):
            day = fromDate + timedelta(days=i)
            for each in allBookingList:  
                if ((fromTime >= each.start_time and fromTime <= each.end_time) or 
                    (toTime >= each.start_time and toTime <= each.end_time)) and each.bookdate == day:
                    state = 0  
                    break
        if state == 0:
            errorMsg = 'เวลาไม่ถูกต้อง Range'
            self.add_error('fromTime', errorMsg)
            print('Time-error Range')
            