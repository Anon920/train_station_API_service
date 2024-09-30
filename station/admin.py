from django.contrib import admin
from .models import Train, TrainType, Station, Route, Journey

admin.site.register(Train)
admin.site.register(TrainType)
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Journey)

