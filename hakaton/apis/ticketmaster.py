from datetime import timedelta

from django.utils.datetime_safe import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from hakaton.models import Customer

from hakaton.apis import api

time_format = "%Y-%m-%dT%H:%M:%SZ"


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
    user = Customer.objects.get(id=user_id)
    likes = user.saved_likes()
    start_date_time = datetime.now()
    end_date_time = datetime.now() + timedelta(days=50)

    all_events = []
    for like in likes:
        params = {'keyword': like,
                  'classificationName': "Music",
                  'countryCode': 'GB',
                  'startDateTime': start_date_time.strftime(time_format),
                  'endDateTime': end_date_time.strftime(time_format)}

        result = api.ticketmaster_api_call(params)
        if '_embedded' in result:
            all_events = all_events + result['_embedded']['events']

    return Response(all_events)


