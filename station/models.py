from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError

from train_station_API_service import settings


class TrainType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=100)
    cargo_num = models.PositiveIntegerField()
    places_in_cargo = models.PositiveIntegerField()
    train_type = models.ForeignKey(TrainType, related_name="trains", on_delete=models.CASCADE)

    def __str__(self):
        return f"Train: {self.name} (id {self.id})"

    class Meta:
        verbose_name_plural = "trains"


class Station(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.latitude} {self.longitude})"

    class Meta:
        verbose_name_plural = "stations"


class Route(models.Model):
    source = models.ForeignKey(Station, related_name="source_routes", on_delete=models.CASCADE)
    destination = models.ForeignKey(Station, related_name="destination_routes", on_delete=models.CASCADE)
    distance = models.PositiveIntegerField()

    def __str__(self):
        return f"Route: {self.source.name} - {self.destination.name}"


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Journey(models.Model):
    route = models.ForeignKey(Route, related_name="route", on_delete=models.CASCADE)
    train = models.ForeignKey(Train, related_name="train", on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="journeys")

    def __str__(self):
        return (f"Journey from {self.route.source} to {self.route.destination}. "
                f"Time: {self.departure_time.strftime("%Y-%m-%d %H:%M:%S")} - "
                f"{self.arrival_time.strftime("%Y-%m-%d %H:%M:%S")}")

    def clean(self):
        if self.departure_time >= self.arrival_time:
            raise ValidationError("Departure time cannot be later than arrival time")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    @property
    def name(self):
        return f"Order {self.id} by {self.user}"


class Ticket(models.Model):
    cargo = models.IntegerField()
    seats = models.IntegerField()
    journey = models.ForeignKey(Journey, related_name="tickets", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="tickets", on_delete=models.CASCADE)

    def __str__(self):
        return f"Ticket {self.id} for {self.journey} (Seats: {self.seats})"
