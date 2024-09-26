from rest_framework import serializers

from station.models import Train


class TrainSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, max_length=100)
    cargo_num = serializers.IntegerField(required=True, min_value=0)

    def create(self, validated_data):
        return Train.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.cargo_num = validated_data.get('cargo_num', instance.cargo_num)
        instance.save()
        return instance
