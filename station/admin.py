from django.contrib import admin
from .models import Train, TrainType, Station

admin.site.register(Train)
admin.site.register(TrainType)
admin.site.register(Station)
