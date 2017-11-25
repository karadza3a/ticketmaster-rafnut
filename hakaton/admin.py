from django.contrib import admin

from .models import Customer, FlightPriceCache, Plan, HotelCache, HotelPriceCache

admin.site.register(Customer)
admin.site.register(Plan)
admin.site.register(FlightPriceCache)
admin.site.register(HotelPriceCache)
admin.site.register(HotelCache)
