from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from station.models import Train
from station.serializers import TrainSerializer


@api_view(["GET", "POST"])
def train_list(request):
    if request.method == 'GET':
        train = Train.objects.all()
        serializer = TrainSerializer(train, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = TrainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def train_detail(request, pk):
    train = get_object_or_404(Train, pk=pk)

    if request.method == 'GET':
        serializer = TrainSerializer(train)
        return Response(serializer.data, status=200)

    if request.method == 'PUT':
        serializer = TrainSerializer(train, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        train.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


