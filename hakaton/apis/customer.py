import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from hakaton.models import Customer, CustomerSerializer, Plan, PlanSerializer


@api_view(http_method_names=['GET', 'POST'])
def customer(request, user_id):
    if request.method == 'GET':
        u, created = Customer.objects.get_or_create(id=user_id)
        return Response(CustomerSerializer(u).data)
    if request.method == 'POST':
        body = json.loads(request.body)
        likes = body['saved_likes']
        u, created = Customer.objects.get_or_create(id=user_id)
        u.set_likes(likes)
        u.save()
        return Response(CustomerSerializer(u).data)


@api_view(http_method_names=['POST'])
def plan(request, user_id):
    body = json.loads(request.body)
    x = body['plan_data']
    plan_data = json.loads(x)
    u, created = Customer.objects.get_or_create(id=user_id)
    p = Plan()
    p.customer = u
    p.plan_data = json.dumps(plan_data)
    p.save()
    return Response(PlanSerializer(p).data)


@api_view(http_method_names=['GET'])
def get_plan(request, plan_id):
    p = Plan.objects.get(id=plan_id)
    js = json.loads(p.plan_data)
    return Response(js)


@api_view(http_method_names=['GET'])
def get_plans(request, user_id):
    ps = Plan.objects.filter(customer__id=user_id)
    return Response([PlanSerializer(plan).data for plan in ps])
