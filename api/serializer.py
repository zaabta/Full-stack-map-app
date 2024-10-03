from rest_framework import serializers
from .models import Order, Job

class OrderSerializers(serializers.ModelSerializer):
    class Mate:
        model=Order
        fields='__all__'

class JobSerializes(serializers.ModelSerializer):
    class Mate:
        model=Job
        fields='__all__'
        