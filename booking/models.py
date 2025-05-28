from django.db import models
from django.utils import timezone
from datetime import datetime, time
from django.utils.timezone import make_aware, now

class Airport(models.Model):
    code = models.CharField(max_length=4, unique=True)  # e.g., 'NZNE'
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True)
    timezone = models.CharField(max_length=50, null=True)  # e.g., 'Pacific/Auckland'

    def __str__(self):
        return f"{self.code} - {self.name}"

class Aircraft(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

def today_midnight():
    return make_aware(datetime.combine(now().date(), time.min))

class ScheduledFlight(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    capacity = models.IntegerField(default=10)
    flight_number = models.CharField(max_length=10)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    origin = models.ForeignKey(Airport, related_name='departures', on_delete=models.CASCADE, null=True)
    destination = models.ForeignKey(Airport, related_name='arrivals', on_delete=models.CASCADE, null=True)
    departure_time = models.DateTimeField(default=today_midnight)  # <-- Add default here
    arrival_time = models.DateTimeField(null=True, default=today_midnight)  # optional, if you want it to default too
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.flight_number}: {self.origin} → {self.destination}"

class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    flight_time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.origin} to {self.destination}"

class Booking(models.Model):
    scheduled_flight = models.ForeignKey(ScheduledFlight, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    reference_code = models.CharField(max_length=10, unique=True)
    booking_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.reference_code} - {self.customer_name}"


