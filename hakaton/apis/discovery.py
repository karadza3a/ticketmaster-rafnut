import json
from datetime import timedelta, datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from hakaton import mail
from hakaton.apis import ticketmaster
from hakaton.models import Plan

time_format = "%Y-%m-%d"
time_format_ticketmaster = "%Y-%m-%dT%H:%M:%SZ"
time_format_airplane = "%Y-%m-%dT%H:%M"


@api_view(http_method_names=['GET'])
def find_event(request, plan_id):
    plan_model = Plan.objects.get(id=plan_id)
    plan = json.loads(plan_model.plan_data)
    start_date = datetime.strptime(plan["event"]["datetime"], time_format_ticketmaster) + timedelta(days=1)
    end_date = datetime.strptime(plan['flight']["inbound"]["flights"][-1]["departs_at"],
                                 time_format_airplane) - timedelta(days=1)

    events = []
    radius = 30
    while True:
        if len(events) == 0 and radius < 300:
            events = ticketmaster.upsell_event_helper(start_date.strftime(time_format_ticketmaster),
                                                      end_date.strftime(time_format_ticketmaster),
                                                      plan["accomodation"]["location"]["latitude"],
                                                      plan["accomodation"]["location"]["longitude"],
                                                      radius)
            radius += 30
        else:
            break

    name = events[0]['name']
    venue = events[0]['venue']['name']
    city = events[0]['venue']['city']['name']
    dt = events[0]['datetime']

    datestring = datetime.strptime(dt, time_format_ticketmaster).strftime("%b %dth at %H:%Mh")
    distance = events[0]['distance']
    pitch = "We found this event you might be interested in:\n%s is performing at %s in %s on %s, just %.1f" \
            " miles away from your hotel." % (name, venue, city, datestring, distance)
    url = events[0]['url']
    img = events[0]['image']['url']

    mail.send_mail(img, pitch, url)

    return Response("ok")
