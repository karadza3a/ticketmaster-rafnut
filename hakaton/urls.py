from django.conf.urls import url

from hakaton.apis import facebook
from hakaton.apis import customer
from hakaton import views

urlpatterns = [
    url(r'^find-booking', views.get_hotel_link, name='find_booking'),
    url(r'^get-hotels', views.get_hotels, name='nearest_hotels'),
    url(r'^get-flights', views.get_flights, name='nearest_flights'),
    url(r'^facebook/likes', facebook.likes),
    url(r'^customer/(?P<user_id>[0-9]+)$', customer.customer)
]
