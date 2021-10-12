from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class Address(models.Model):
    formatted_address = models.CharField(max_length=200, blank=True, null=True)
    place_id = models.CharField(max_length=32, blank=True, null=True)
    type_of_address = models.CharField(max_length=200, blank=True, null=True)


class Timeslot(models.Model):
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    type_of_address = models.CharField(max_length=200, blank=True, null=True)


class Delivery(models.Model):
    user = models.CharField(max_length=32)
    status = models.CharField(max_length=8)
    timeslot = models.ForeignKey(Timeslot, on_delete=CASCADE)
