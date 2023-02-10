from rest_framework import serializers
from .models import NidanTicket

class NidanSolvedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NidanTicket
        fields = '__all__'
