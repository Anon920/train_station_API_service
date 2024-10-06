from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from station.models import Train, TrainType, Station, Route, Journey, Crew, Order, Ticket
from station.serializers import TrainSerializer, TrainTypeSerializer, StationSerializer, RouteSerializer, \
    JourneySerializer, TrainListSerializer, RouteListSerializer, TrainRetrieveSerializer, RouteRetrieveSerializer, \
    JourneyListSerializer, JourneyRetrieveSerializer, CrewSerializer, OrderSerializer, TicketSerializer, \
    TicketListSerializer, TicketRetrieveSerializer, OrderListSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all().select_related("train_type")

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
    queryset = Crew.objects.all().select_related()
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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        return Response({"detail": "POST method is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related("journey", "order")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        elif self.action == "retrieve":
            return TicketRetrieveSerializer
        return TicketSerializer

    def perform_create(self, serializer):
        user = self.request.user
        journey = serializer.validated_data['journey']

        existing_order = Order.objects.filter(user=user).first()

        if existing_order and Ticket.objects.filter(order=existing_order, journey=journey).exists():
            serializer.save(order=existing_order)
        else:
            new_order = Order.objects.create(user=user)
            serializer.save(order=new_order)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        else:
            return Ticket.objects.filter(order__user=user)
