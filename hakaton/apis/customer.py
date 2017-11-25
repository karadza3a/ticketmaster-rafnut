from rest_framework.decorators import api_view
from rest_framework.response import Response

from hakaton.models import Customer, CustomerSerializer


@api_view(http_method_names=['GET', 'POST'])
def customer(request, user_id):
    if request.method == 'GET':
        u = Customer.objects.get(id=user_id)
        return Response(CustomerSerializer(u).data)
    if request.method == 'POST':
        likes = request.POST['saved_likes']
        u, created = Customer.objects.get_or_create(id=user_id)
        u.set_likes(likes)
        u.save()
        return Response(CustomerSerializer(u).data)
