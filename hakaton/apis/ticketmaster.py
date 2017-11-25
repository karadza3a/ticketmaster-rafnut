from datetime import timedelta

from django.utils.datetime_safe import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
