import random
from datetime import timedelta, datetime
from math import sin, cos, sqrt, atan2, radians

import Geohash
from django.utils.datetime_safe import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hakaton.apis import api
from hakaton.models import Customer, FlightPriceCache, HotelPriceCache, Plan

time_format = "%Y-%m-%dT%H:%M:%SZ"


def dist(lat, lng, dest_lat, dest_lng):
    R = 6373.0

    lat1 = radians(lat)
    lon1 = radians(lng)
    lat2 = radians(dest_lat)
    lon2 = radians(dest_lng)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def flights_starting_from(lat, lng, dlat, dlng):
    if dist(lat, lng, dlat, dlng) < 200:
        return 0

    min_dist = 9999999999
    min_price = -1

    for pc in FlightPriceCache.objects.all():
        slat, slon, elat, elon = pc.start_lat, pc.start_lng, pc.end_lat, pc.end_lng
        d1 = dist(lat, lng, slat, slon) + dist(dlat, dlng, elat, elon)
        d2 = dist(lat, lng, elat, elon) + dist(dlat, dlng, slat, slon)
        if min_dist > min(d1, d2):
            min_dist = min(d1, d2)
            min_price = pc.price

    return min_price


def hotels_starting_from(lat, lng):
    min_price = 99999999

    for pc in HotelPriceCache.objects.all():
        d = dist(lat, lng, pc.lat, pc.lng)
        if d < 50:
            min_price = min(pc.price, min_price)
    if min_price == 99999999:
        min_price = random.randint(44, 123) + random.randint(1, 99) / 100.

    return min_price


@api_view(http_method_names=['GET'])
def events(request):
    start_date_time = datetime.now()
    end_date_time = datetime.now() + timedelta(days=10)
    keyword = request.GET['keyword']
    params = {'keyword': keyword,
              'classificationName': "Music",
              'countryCode': 'GB',
              'startDateTime': start_date_time.strftime(time_format),
              'endDateTime': end_date_time.strftime(time_format)}

    result = api.ticketmaster_api_call(params)

    print(result)

    res2 = []
    if '_embedded' in result:
        res2 = [(y['name'], y['dates']['start']['localDate']) for y in result['_embedded']['events']]

    return Response(res2)


@api_view(http_method_names=['GET'])
def real_events(request):
    user_id = request.GET["id"]
    lat = float(request.GET["lat"])
    lng = float(request.GET["lon"])
    user = Customer.objects.get(id=user_id)
    likes = user.saved_likes()
    start_date_time = datetime.strptime(request.GET["startTime"], "%Y-%m-%d")
    end_date_time = datetime.strptime(request.GET["endTime"], "%Y-%m-%d")

    all_bands = []
    for like in likes:
        params = {'keyword': like,
                  'classificationName': "Music",
                  'countryCode': 'GB',
                  'startDateTime': start_date_time.strftime(time_format),
                  'endDateTime': end_date_time.strftime(time_format)}

        result = api.ticketmaster_api_call(params)
        if '_embedded' in result:
            all_bands.append({
                'events': result['_embedded']['events'],
                'name': like
            })

    for band in all_bands:
        for event in band['events']:
            maxw = 0
            for image in event['images']:
                if image['width'] > maxw:
                    maxw = image['width']
                    event['image'] = image
            event.pop('images', None)

            event.pop('seatmap', None)
            event.pop('test', None)
            event.pop('promoters', None)
            event.pop('info', None)
            event.pop('pleaseNote', None)
            event.pop('sales', None)
            event.pop('promoters', None)
            event.pop('promoter', None)
            event.pop('ada', None)

            event['datetime'] = event['dates']["start"]["dateTime"]
            event.pop('dates', None)

            venue = event['_embedded']['venues'][0]
            venue.pop('boxOfficeInfo', None)
            venue.pop('parkingDetail', None)
            venue.pop('accessibleSeatingDetail', None)
            venue.pop('generalInfo', None)
            venue.pop('upcomingEvents', None)
            venue.pop('ada', None)
            venue.pop('markets', None)
            venue.pop('dmas', None)
            venue.pop('test', None)
            venue.pop('images', None)
            event['venue'] = venue
            event.pop('_embedded')

            dest_lat = float(venue['location']['latitude'])
            dest_lng = float(venue['location']['longitude'])
            event['flightsStartingFrom'] = flights_starting_from(lat, lng, dest_lat, dest_lng)
            event['hotelsStartingFrom'] = hotels_starting_from(dest_lat, dest_lng)

    print(all_bands)

    return Response(all_bands)


@api_view(http_method_names=['GET'])
def upsell_event(request, plan_id):
    p = Plan.objects.get(id=plan_id)

    start_date_time = p.plan_data
    start_date_time = datetime.strptime(request.GET["startTime"], "%Y-%m-%d")
    end_date_time = datetime.strptime(request.GET["endTime"], "%Y-%m-%d")
    start = start_date_time.strftime(time_format)
    end = end_date_time.strftime(time_format)
    lat = float(request.GET["lat"])
    lng = float(request.GET["lon"])
    radius = 30

    result = upsell_event_helper(start, end, lat, lng, radius)
    while True:
        if len(result) == 0 and radius < 300:
            radius += 30
            result = upsell_event_helper(start, end, lat, lng, radius)
        else:
            break
    print(result)
    return Response(result)


def upsell_event_helper(start, end, lat, lng, radius):
    params = {'classificationName': "Music",
              'size': 1,
              'countryCode': 'GB',
              'startDateTime': start,
              'endDateTime': end,
              'geoPoint': Geohash.encode(lat, lng, precision=9),
              'radius': radius,
              }

    result = api.ticketmaster_api_call(params)

    if '_embedded' not in result:
        return []

    for event in result['_embedded']['events']:
        maxw = 0
        for image in event['images']:
            if image['width'] > maxw:
                maxw = image['width']
                event['image'] = image
        event.pop('images', None)

        event.pop('seatmap', None)
        event.pop('test', None)
        event.pop('promoters', None)
        event.pop('info', None)
        event.pop('pleaseNote', None)
        event.pop('sales', None)
        event.pop('promoters', None)
        event.pop('promoter', None)
        event.pop('ada', None)

        event['datetime'] = event['dates']["start"]["dateTime"]
        event.pop('dates', None)

        venue = event['_embedded']['venues'][0]
        venue.pop('boxOfficeInfo', None)
        venue.pop('parkingDetail', None)
        venue.pop('accessibleSeatingDetail', None)
        venue.pop('generalInfo', None)
        venue.pop('upcomingEvents', None)
        venue.pop('ada', None)
        venue.pop('markets', None)
        venue.pop('dmas', None)
        venue.pop('test', None)
        venue.pop('images', None)
        event['venue'] = venue
        event.pop('_embedded')

    result = result['_embedded']['events']
    return result
