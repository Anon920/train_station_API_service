from django.db import models
from rest_framework.exceptions import ValidationError


class TrainType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=100)
    cargo_num = models.PositiveIntegerField()
    places_in_cargo = models.PositiveIntegerField()
    train_type = models.ForeignKey(TrainType, related_name="train_type", on_delete=models.CASCADE)

    def __str__(self):
        return f"Train: {self.name} (id {self.id})"

    class Meta:
        verbose_name_plural = "trains"


class Station(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Station: {self.name} ({self.latitude} {self.longitude})"

    class Meta:
        verbose_name_plural = "stations"


class Route(models.Model):
    source = models.ForeignKey(Station, related_name="source", on_delete=models.CASCADE)
    destination = models.ForeignKey(Station, related_name="destination", on_delete=models.CASCADE)
    distance = models.PositiveIntegerField()

    def __str__(self):
        return f"Route: {self.source.name} - {self.destination.name}"


class Journey(models.Model):
    route = models.ForeignKey(Route, related_name="route", on_delete=models.CASCADE)
    train = models.ForeignKey(Train, related_name="train", on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"Journey: {self.route} - {self.train.name}"

    def clean(self):
        if self.departure_time >= self.arrival_time:
            raise ValidationError("Departure time cannot be later than arrival time")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
