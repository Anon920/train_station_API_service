from django.urls import path, include
from rest_framework import routers

from station.views import TrainViewSet, TrainTypeViewSet, StationViewSet

router = routers.DefaultRouter()
router.register('trains', TrainViewSet)
router.register('trains_types', TrainTypeViewSet)
router.register('stations', StationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

app_name = "station"
