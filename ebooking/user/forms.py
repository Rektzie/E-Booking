from builtins import object
from tkinter import Widget

from django import forms
from user.models import Room_type


class EditForm(forms.Form):
    name = forms.CharField(max_length=255)
    date = forms.DateField()
    
class AddRoomForm(forms.Form):
    roomTypeChoices = [Room_type.objects.values('id'), Room_type.objects.values('name')]
    name = forms.CharField(label='ชื่อห้อง' ,max_length=30, required=True)
    typeselect = forms.ChoiceField(widget=forms.Select, choices=roomTypeChoices)
    start_time = forms.TimeField(required=True)
    end_time = forms.TimeField(required=True)
    capacity = forms.IntegerField(required=True)
    
    
