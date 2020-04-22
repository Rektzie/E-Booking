from builtins import object
from tkinter import Widget

from django import forms
from user.models import Room_type


class EditForm(forms.Form):
    name = forms.CharField(max_length=255)
    date = forms.DateField()
    
    
class TimeInput(forms.TimeInput):
    input_type = 'time'    
    
class AddRoomForm(forms.Form):
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


