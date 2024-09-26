from rest_framework import generics

from station.models import Train
from station.serializers import TrainSerializer


class TrainListView(generics.ListCreateAPIView):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


class TrainDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


