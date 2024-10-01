from django.urls import path, include
from rest_framework import routers

from station.views import TrainViewSet, TrainTypeViewSet, StationViewSet, RouteViewSet, JourneyViewSet, CrewViewSet

router = routers.DefaultRouter()
router.register('trains', TrainViewSet)
router.register('trains_types', TrainTypeViewSet)
router.register('stations', StationViewSet)
router.register("routes", RouteViewSet)
router.register("journey", JourneyViewSet)
router.register("crew", CrewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

app_name = "station"
