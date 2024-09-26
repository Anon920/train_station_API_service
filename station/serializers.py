from rest_framework import serializers

from station.models import Train, TrainType


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ("id", "name", "cargo_num", "places_in_cargo")
        read_only_fields = ("id", )
