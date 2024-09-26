from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from station.models import Train
from station.serializers import TrainSerializer


@api_view(["GET", "POST"])
def train_list(request):
    if request.method == 'GET':
        trains = Train.objects.all()
        serializer = TrainSerializer(trains, many=True)
        return Response(serializer.data, status=200)

    if request.method == 'POST':
        serializer = TrainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
