import json
from datetime import datetime, timedelta

from rest_framework.decorators import api_view
from rest_framework.response import Response

from hakaton.apis import ticketmaster
from hakaton.models import Plan

time_format = "%Y-%m-%d"
time_format_ticketmaster = "%Y-%m-%dT%H:%M:%SZ"


@api_view(http_method_names=['GET'])
def find_event(request, plan_id):
    plan_model = Plan.objects.get(id=plan_id)
    plan = json.loads(plan_model.plan_data)
    start_date = datetime.strptime(plan["event"]["date"], time_format) + timedelta(days=1)
    end_date = datetime.strptime(plan["end_date"], time_format) - timedelta(days=1)

    events = []
    radius = 30
    while True:
        if len(events) == 0 and radius < 300:
            events = ticketmaster.upsell_event_helper(start_date.strftime(time_format_ticketmaster),
                                                      end_date.strftime(time_format_ticketmaster),
                                                      plan["hotel"]["lat"],
                                                      plan["hotel"]["lon"],
                                                      radius)
            radius += 30
        else:
            break

    print(events[0])
    return Response(events[0])
