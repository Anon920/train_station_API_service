from django.urls import path

from station.views import train_list, train_detail

urlpatterns = [
    path("trains/", train_list, name="train-list"),
    path("trains/<int:pk>/", train_detail, name="train-detail"),
]

app_name = "station"
