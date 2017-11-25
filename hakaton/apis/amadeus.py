from hakaton.apis import api
import datetime

amadeus_key = "jldrRx5RICjLd3yBqK1DHtto6eGxbAZm"

url_airport_nearest = "https://api.sandbox.amadeus.com/v1.2/airports/nearest-relevant"
url_flight_low_fare = "https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search"
url_hotels_circle = "https://api.sandbox.amadeus.com/v1.2/hotels/search-box"
url_train_search = "https://api.sandbox.amadeus.com/v1.2/trains/schedule-search"


def send_request(url, params):
    return api.api_call(url + "?apikey=" + amadeus_key + "&", params)


def find_nearest_airport(lat, lon):
    airports = send_request(url_airport_nearest, {"latitude": lat, "longitude": lon})
    sorted_airports = sorted(airports, key=lambda k: k['distance'])
    return sorted_airports[0]


def find_near_hotel(lat, lon, check_in, check_out):
    hotels = send_request(url_hotels_circle, {"south_west_corner": str(float(lat)-0.05)+","+str(float(lon)-0.05),
                                              "north_east_corner": str(float(lat)+0.05)+","+str(float(lon)+0.05),
                                              "check_in": check_in,
                                              "check_out": check_out,
                                              "radius": 20})
    return hotels


def find_flight(origin_lat, origin_lon, dest_lat, dest_lon, departure_date, return_date, num_of_seats=1):
    origin_airport = find_nearest_airport(origin_lat, origin_lon)
    destination_airport = find_nearest_airport(dest_lat, dest_lon)

    params = {"currency": "EUR",
              "origin": origin_airport["city"],
              "destination": destination_airport["city"],
              "departure_date": departure_date,
              "return_date": return_date
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

    return results
