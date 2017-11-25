from rest_framework.decorators import api_view
from rest_framework.response import Response

from hakaton.apis import amadeus
from hakaton.apis import google


@api_view(http_method_names=['GET'])
def get_flights(request):
    results = amadeus.find_flight(request.GET['originLat'],
                                  request.GET['originLon'],
                                  request.GET['destLat'],
                                  request.GET['destLon'],
                                  request.GET['departureDate'],
                                  request.GET['returnDate'],
                                  request.GET['passengers'])

    return Response(results)


@api_view(http_method_names=['GET'])
def get_hotels(request):
    results = amadeus.find_near_hotel(request.GET['lat'],
                                      request.GET['lon'],
                                      request.GET['checkIn'],
                                      request.GET['checkOut'])

    return Response(results)


@api_view(http_method_names=['GET'])
def get_hotel_link(request):
    results = google.get_booking_link(request.GET['name'])

    return Response(results)
