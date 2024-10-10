from django.db import transaction
from rest_framework import serializers

from station.models import Train, TrainType, Station, Route, Journey, Crew, Order, Ticket


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ("id", "name", "cargo_num", "places_in_cargo", "train_type")


class TrainListSerializer(TrainSerializer):
    train_type = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )


class TrainRetrieveSerializer(TrainSerializer):
    train_type = TrainTypeSerializer(many=False)


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

    def validate(self, attrs):
        if attrs["destination"] == attrs["source"]:
            raise serializers.ValidationError("The destination and source cannot be the same.")
        return attrs


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )
    destination = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )


class RouteRetrieveSerializer(RouteSerializer):
    source = StationSerializer(many=False)
    destination = StationSerializer(many=False)


class JourneySerializer(serializers.ModelSerializer):
    departure_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    arrival_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Journey
        fields = ("id", "route", "train", "departure_time", "arrival_time", "crew")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "id", "first_name", "last_name"


class JourneyListSerializer(JourneySerializer):
    route = serializers.SerializerMethodField()
    train = serializers.CharField(source='train.name', read_only=True)
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='full_name'
    )

    def get_route(self, obj):
        return f"{obj.route.source.name} - {obj.route.destination.name}"


class JourneyRetrieveSerializer(JourneySerializer):
    route = RouteRetrieveSerializer(many=False)
    train = TrainRetrieveSerializer(many=False)
    crew = CrewSerializer(many=True, read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "user")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seats", "journey")


class TicketListSerializer(TicketSerializer):
    journey = serializers.CharField(source="journey.route", read_only=True)
    order = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seats", "journey", "order")

    def validate(self, attrs):
        journey = attrs.get('journey')
        seats = attrs.get('seats')
        cargo = attrs.get('cargo')

        if Ticket.objects.filter(journey=journey, seats=seats).exists():
            raise serializers.ValidationError(f"Seat {seats} already exist.")

        if journey:
            available_cargo = journey.train.available_cargo

            if cargo > available_cargo:
                raise serializers.ValidationError(f"Cargo {cargo} exceeds available capacity of {available_cargo}.")

        return attrs


class TicketRetrieveSerializer(TicketListSerializer):
    journey = JourneyRetrieveSerializer(many=False)
    order = OrderSerializer(many=False)


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "tickets")
