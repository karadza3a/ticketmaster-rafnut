from django.conf.urls import url

from hakaton.apis import facebook
from hakaton.apis import customer
from hakaton import views

urlpatterns = [
    url(r'^nearest', views.nearest_airport, name='nearest'),
    url(r'^facebook/likes', facebook.likes),
    url(r'^customer/(?P<user_id>[0-9]+)$', customer.customer)
]
