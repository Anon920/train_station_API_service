from django.db import models


class Train(models.Model):
    name = models.CharField(max_length=100)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()

    def __str__(self):
        return f"Train: {self.name} (id {self.id})"

    class Meta:
        verbose_name_plural = "trains"


