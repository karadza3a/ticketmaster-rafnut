from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime

from hakaton import api
from hakaton import amadeus

time_format = "%Y-%m-%dT%H:%M:%SZ"


@api_view(http_method_names=['GET'])
def test(request, classifications="Music", start_date_time=datetime.datetime.now(),
         end_date_time=datetime.datetime.now() + datetime.timedelta(days=10)):
    pages = api.ticketmaster_api_call({
        'classifications': classifications,
        'countryCode': 'GB',
        'startDateTime': start_date_time.strftime(time_format),
        'endDateTime': end_date_time.strftime(time_format)
    })

    return Response(pages)


@api_view(http_method_names=['GET'])
def nearest_airport(request):

    results = amadeus.find_flight(request.GET['originLat'],
                                  request.GET['originLon'],
                                  request.GET['destLat'],
                                  request.GET['destLon'],
                                  request.GET['departureDate'],
                                  request.GET['returnDate'],
                                  request.GET['passengers'])

    return Response(results)
