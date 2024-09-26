from rest_framework.response import Response

from station.models import Train
from station.serializers import TrainSerializer


def train_list(request):
    if request.method == 'GET':
        trains = Train.objects.all()
        serializer = TrainSerializer(trains, many=True)
        return Response(serializer.data)
