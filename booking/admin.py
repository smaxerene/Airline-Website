from django.contrib import admin
from .models import Airport, Aircraft, ScheduledFlight

admin.site.register(Airport)
admin.site.register(Aircraft)
admin.site.register(ScheduledFlight)
