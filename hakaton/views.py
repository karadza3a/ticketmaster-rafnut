from rest_framework.decorators import api_view
from rest_framework.response import Response

from hakaton.apis import amadeus


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
