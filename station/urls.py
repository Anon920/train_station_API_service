from django.urls import path, include
from rest_framework import routers

from station.views import TrainViewSet, TrainTypeViewSet

router = routers.DefaultRouter()
router.register('trains', TrainViewSet)
router.register('trains_types', TrainTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

app_name = "station"
