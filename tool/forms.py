from django.forms import ModelForm
from .models import Ticket,Operator
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class OperatorProfile(ModelForm):
    class Meta:
        model = Operator
        field = '__all__'
        exclude = ['user']

class UserRegistrationForm(UserCreationForm):
      class Meta:
        model =User 
        fields = ['username','first_name','last_name','email']


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        exclude =['creatd_by',]
        widgets = {
            'description':forms.Textarea(attrs={'cols': '60', 'rows': '3','description':'description'})
        }

        
