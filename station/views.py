from rest_framework import viewsets

from station.models import Train, TrainType, Station, Route, Journey, Crew
from station.serializers import TrainSerializer, TrainTypeSerializer, StationSerializer, RouteSerializer, \
    JourneySerializer, TrainListSerializer, RouteListSerializer, TrainRetrieveSerializer, RouteRetrieveSerializer, \
    JourneyListSerializer, JourneyRetrieveSerializer, CrewSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all().select_related()

    def get_serializer_class(self):
        if self.action == 'list':
            return TrainListSerializer
        if self.action == 'retrieve':
            return TrainRetrieveSerializer
        return TrainSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == ("list", "retrieve"):
            queryset = queryset.select_related("train_type")
        return queryset


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().select_related()

    def get_serializer_class(self):
        if self.action == 'list':
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteRetrieveSerializer
        return RouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = queryset.select_related("source", "destination")
        return queryset


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all().select_related()

    def get_serializer_class(self):
        if self.action == 'list':
            return JourneyListSerializer
        if self.action == "retrieve":
            return JourneyRetrieveSerializer
        return JourneySerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = queryset.select_related("route", "train")
        return queryset


