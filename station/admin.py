from django.contrib import admin
from .models import Train, TrainType, Station, Route

admin.site.register(Train)
admin.site.register(TrainType)
admin.site.register(Station)
admin.site.register(Route)
