from django.urls import path

from station.views import train_list


urlpatterns = [
    path("trains/", train_list, name="train-list"),
]

app_name = "station"
