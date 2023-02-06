from django.contrib import admin
from .models import Ticket,Operator,NidanTicket
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget
# Register your models here.
admin.site.register(Operator)
admin.site.register(NidanTicket)


class CallerForm(forms.ModelForm):
    class Meta:
        widgets = {
            'phone':PhoneNumberPrefixWidget(initial='IN'),
        }


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    form = CallerForm