from rest_framework import serializers

from .models import Cardpayment




class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardpayment
        fields = ['name','email','phone','address','bill',]  