import datetime
from math import sin, cos, sqrt, atan2, radians

from hakaton.apis import api
from hakaton.models import FlightPriceCache, HotelCache, HotelPriceCache

amadeus_key = "jldrRx5RICjLd3yBqK1DHtto6eGxbAZm"

url_airport_nearest = "https://api.sandbox.amadeus.com/v1.2/airports/nearest-relevant"
url_flight_low_fare = "https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search"
url_hotels_circle = "https://api.sandbox.amadeus.com/v1.2/hotels/search-box"
url_train_search = "https://api.sandbox.amadeus.com/v1.2/trains/schedule-search"


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


def send_request(url, params):
    return api.api_call(url + "?apikey=" + amadeus_key + "&", params)


def find_nearest_airport(lat, lon):
    airports = send_request(url_airport_nearest, {"latitude": lat, "longitude": lon})
    sorted_airports = sorted(airports, key=lambda k: k['distance'])
    return sorted_airports[0]


def find_near_hotel(lat, lon, check_in, check_out):
    for hotel in HotelCache.objects.all():
        if dist(float(lat), float(lon), hotel.lat, hotel.lng) < 15:
            return hotel.json_value

    hotels = send_request(url_hotels_circle,
                          {"south_west_corner": str(float(lat) - 0.05) + "," + str(float(lon) - 0.05),
                           "north_east_corner": str(float(lat) + 0.05) + "," + str(float(lon) + 0.05),
                           "check_in": check_in,
                           "check_out": check_out,
                           "number_of_results": 3
                           })

    h = HotelCache()
    h.json_value = hotels
    h.lat = lat
    h.lng = lon
    h.save()

    p = min([r['total_price']['amount'] for r in hotels['results']])
    pc = HotelPriceCache()
    pc.lat = lat
    pc.lng = lon
    pc.price = p
    pc.save()

    return hotels


def find_flight(origin_lat, origin_lon, dest_lat, dest_lon, departure_date, return_date, num_of_seats=1):
    origin_airport = find_nearest_airport(origin_lat, origin_lon)
    destination_airport = find_nearest_airport(dest_lat, dest_lon)

    params = {"currency": "EUR",
              "origin": origin_airport["city"],
              "destination": destination_airport["city"],
              "departure_date": departure_date,
              "return_date": return_date,
              "number_of_results": 5
              }

    results = send_request(url_flight_low_fare, params)

    for result in results["results"]:
        itineraries = result["itineraries"]
        for itinerary in itineraries:
            flights = itinerary["outbound"]["flights"]
            f = flights[0]["origin"]["airport"]
            t = flights[-1]["destination"]["airport"]
            start_date = datetime.datetime.strptime(flights[0]["departs_at"], "%Y-%m-%dT%H:%M")
            sel = ""
            for flight in flights:
                depart_date = datetime.datetime.strptime(flight["departs_at"], "%Y-%m-%dT%H:%M")
                sel = (sel +
                       flight["origin"]["airport"] +
                       flight["destination"]["airport"] +
                       str(depart_date.day - start_date.day) +
                       flight["marketing_airline"] +
                       flight["flight_number"] +
                       "-")

            if sel[-1] == "-":
                sel = sel[:-1]

            itinerary["url"] = ("https://www.google.rs/flights/#search;f=" + f +
                                ";t=" + t +
                                ";d=" + departure_date +
                                ";r=" + return_date +
                                ";px=" + str(num_of_seats) +
                                ";sel=" + sel
                                )

    p = min([r['fare']['total_price'] for r in results['results']])
    pc = FlightPriceCache()
    pc.start_lat = origin_lat
    pc.start_lng = origin_lon
    pc.end_lat = dest_lat
    pc.end_lng = dest_lon
    pc.price = p
    pc.save()

    return results
