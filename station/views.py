from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

from station.models import Train, TrainType, Station, Route, Journey, Crew
from station.serializers import TrainSerializer, TrainTypeSerializer, StationSerializer, RouteSerializer, \
    JourneySerializer, TrainListSerializer, RouteListSerializer, TrainRetrieveSerializer, RouteRetrieveSerializer, \
    JourneyListSerializer, JourneyRetrieveSerializer, CrewSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all().select_related()
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
        train_type = self.request.query_params.getlist('train_type')
        if train_type:
            queryset = queryset.filter(train_type__id__in=train_type)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="train_type",
                type={"type": "array", "items": {"type": "number"}},
                description="Filter by train type IDs (e.g., ?train_type=2,3)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of trains."""
        return super().list(request, *args, **kwargs)


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all().select_related()
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
        source_name = self.request.query_params.get('source')
        destination_name = self.request.query_params.get('destination')

        if source_name:
            queryset = queryset.filter(source__name__icontains=source_name)
        if destination_name:
            queryset = queryset.filter(destination__name__icontains=destination_name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="source",
                type=str,
                description="Filter by source station name (e.g., ?source=Kyiv)",
                required=False,
            ),
            OpenApiParameter(
                name="destination",
                type=str,
                description="Filter by destination station name (e.g., ?destination=Lviv)",
                required=False,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of routes."""
        return super().list(request, *args, **kwargs)


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
