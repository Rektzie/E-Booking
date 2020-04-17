from django import forms

class EditForm(forms.Form):
    name = forms.CharField(max_length=255)
    date = forms.DateField()
    
