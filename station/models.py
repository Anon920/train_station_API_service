from django.db import models


class TrainType(models.Model):
    name = models.CharField(max_length=100)

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
    name = models.CharField(max_length=100)
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

    class Meta:
        unique_together = (("source", "destination"),)

