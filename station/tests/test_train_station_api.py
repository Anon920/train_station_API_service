from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from station.models import TrainType, Train, Station, Route, Crew, Journey
from station.serializers import StationSerializer, TrainListSerializer, TrainRetrieveSerializer

STATION_URL = reverse("station:station-list")
TRAIN_URL = reverse("station:train-list")


def sample_train(**params):
    train_type_name = params.get("train_type_name", "Test train")
    train_type, created = TrainType.objects.get_or_create(name=train_type_name)

    defaults = {
        "name": "Test train",
        "cargo_num": 150,
        "places_in_cargo": 10,
        "train_type": train_type,
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


class AuthenticatedTrainStationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_station_list(self):
        sample_station(name="Kyiv")
        sample_station(name="Lviv")

        res = self.client.get(STATION_URL)

        stations = Station.objects.order_by("id")
        serializer = StationSerializer(stations, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_station_detail(self):
        station = sample_station(name="Kyiv")

        url = reverse("station:station-detail", args=[station.id])

        res = self.client.get(url)

        serializer = StationSerializer(station)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_train_list(self):
        sample_train()
        sample_train()

        res = self.client.get(TRAIN_URL)

        trains = Train.objects.order_by("id")
        serializer = TrainListSerializer(trains, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_train_detail(self):
        train = sample_train()

        url = reverse("station:train-detail", args=[train.id])

        res = self.client.get(url)

        serializer = TrainRetrieveSerializer(train)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
