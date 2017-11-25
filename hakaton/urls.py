from django.conf.urls import url

from hakaton.apis import facebook
from hakaton.apis import customer

urlpatterns = [
    url(r'^facebook/likes', facebook.likes),
    url(r'^customer/(?P<user_id>[0-9]+)$', customer.customer),
]
