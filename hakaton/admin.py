from django.contrib import admin

from .models import Customer, FlightPriceCache

admin.site.register(Customer)
admin.site.register(FlightPriceCache)
