from rest_framework import serializers
from .models import Order, Job

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'

class JobSerializes(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields='__all__'
        