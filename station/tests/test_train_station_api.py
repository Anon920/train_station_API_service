from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from station.models import TrainType, Train, Station, Route, Crew, Journey
from station.serializers import StationSerializer

STATION_URL = reverse("station:station-list")
TRAIN_URL = reverse("station:train-list")


def sample_train_type(**params):
    defaults = {
        "name": "Test train type"
    }
    defaults.update(params)
    return TrainType.objects.create(**defaults)


def sample_train(**params):
    defaults = {
        "name": "Test train",
        "cargo_num": 150,
        "places_in_cargo": 10,
        "train_type": sample_train_type()
    }
    defaults.update(params)
    return Train.objects.create(**defaults)


def sample_station(**params):
    defaults = {
        "name": "Test station",
        "latitude": 50.5,
        "longitude": 40.4,
    }
    defaults.update(params)
    return Station.objects.create(**defaults)


def sample_route(**params):
    defaults = {
        "source": sample_station(),
        "destination": sample_station(),
        "distance": 1000,
    }
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_crew(**params):
    defaults = {
        "first_name": "John",
        "last_name": "Doe"
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_journey(**params):
    defaults = {
        "route": sample_route(),
        "train": sample_train(),
        "departure_time": datetime(2024, 10, 8, 23, 0),
        "arrival_time": datetime(2024, 10, 9, 10, 0),
    }
    defaults.update(params)
    journey = Journey.objects.create(**defaults)
    journey.crew.set([sample_crew()])
    return journey


class UnauthenticatedTrainStationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_station(self):
        res = self.client.get(STATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_for_trains(self):
        res = self.client.get(TRAIN_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
