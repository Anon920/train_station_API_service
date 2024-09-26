from rest_framework import viewsets

from station.models import Train
from station.serializers import TrainSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


