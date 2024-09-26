from django.urls import path

from station.views import TrainListView, TrainDetailView

urlpatterns = [
    path("trains/", TrainListView.as_view(), name="train-list"),
    path("trains/<int:pk>/", TrainDetailView.as_view(), name="train-detail"),
]

app_name = "station"
