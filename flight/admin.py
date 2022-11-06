from django.contrib import admin

from flight.models import Destination
from flight.models import Detailed_desc

# Register your models here.
admin.site.register(Destination)
admin.site.register(Detailed_desc)