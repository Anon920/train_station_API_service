from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from station.models import TrainType, Train, Station, Route, Crew, Journey
from station.serializers import StationSerializer, TrainListSerializer, TrainRetrieveSerializer, RouteListSerializer

STATION_URL = reverse("station:station-list")
TRAIN_URL = reverse("station:train-list")
ROUTE_URL = reverse("station:route-list")


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

    def test_filter_train_by_train_type(self):
        train_type_1 = TrainType.objects.create(name="Test train1")
        train_type_2 = TrainType.objects.create(name="Test train2")

        train_1 = Train.objects.create(
            name="Train A",
            cargo_num=150,
            places_in_cargo=10,
            train_type=train_type_1
        )

        train_2 = Train.objects.create(
            name="Train B",
            cargo_num=150,
            places_in_cargo=10,
            train_type=train_type_2
        )

        res = self.client.get(TRAIN_URL, {'train_type': train_type_1.id})

        trains = Train.objects.filter(train_type=train_type_1)
        serializer = TrainListSerializer(trains, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_route_by_stations(self):
        source = Station.objects.create(name="Test_source", latitude=50, longitude=40)
        destination = Station.objects.create(name="Test_destination", latitude=51, longitude=42)
        Route.objects.create(source=source, destination=destination, distance=1000)

        res_source = self.client.get(ROUTE_URL, {'source': source.name})
        res_destination = self.client.get(ROUTE_URL, {'destination': destination.name})

        routes = Route.objects.filter(source__name=source.name)
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(res_source.status_code, status.HTTP_200_OK)
        self.assertEqual(res_source.data, serializer.data)
        self.assertEqual(res_destination.status_code, status.HTTP_200_OK)
        self.assertEqual(res_destination.data, serializer.data)


class AdminTrainStationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testadminpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_station(self):
        payload = {
            "name": "Test station",
            "latitude": 50,
            "longitude": 40.4,
        }

        res = self.client.post(STATION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        station = Station.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(station, key))
