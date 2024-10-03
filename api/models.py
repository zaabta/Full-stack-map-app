from django.db import models

# Create your models here.


class Status(models.TextChoices):
    READY='RD', 'Ready'
    PENDING='PD', 'Pending'
    DELIVERED = 'DE', 'Delivered' 

class Coordinate(models.Model):
    latitude=models.FloatField()
    longitude=models.FloatField()
    def __str__(self):
        return f'latitude: {self.latitude}, longitude:{self.longitude}'

class Job(models.Model):
    departure_point=models.TextField()
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    pending_order=models.IntegerField(default=0)
    coordinate=models.OneToOneField(Coordinate, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.departure_point

class Order(models.Model):
    job=models.ForeignKey(Job, related_name='orders', on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    phone=models.IntegerField()
    status=models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.READY,
    )
    price=models.DecimalField(max_digits=10, decimal_places=2)
    address=models.TextField()
    duration=models.CharField(max_length=10)
    coordinate=models.OneToOneField(Coordinate, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name