from django.db import models


class TrainType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=100)
    cargo_num = models.PositiveIntegerField()
    places_in_cargo = models.PositiveIntegerField()
    # train_type =

    def __str__(self):
        return f"Train: {self.name} (id {self.id})"

    class Meta:
        verbose_name_plural = "trains"
