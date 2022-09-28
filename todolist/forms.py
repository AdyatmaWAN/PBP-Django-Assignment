from django import forms

class CreateTaskForm(forms.Form):
    tittle = forms.CharField()
    description = forms.CharField()