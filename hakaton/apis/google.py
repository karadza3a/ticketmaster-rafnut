from hakaton.apis import api

google_link = "https://www.googleapis.com/customsearch/v1?key=AIzaSyAInYAui2YTvrqTokSnTBBVgPQcax-oIWI&cx=015881321402431320333:mtaj0xsbxl8&q="


# working, but do not use it!!! (GOOGLE API - 100 queries each day)
def get_booking_link(hotel_name):
    full_url = google_link+hotel_name.replace(" ", "%20")
    print(full_url)
    result = api.api_call(full_url)

    for item in result["items"]:
        if item["link"].startswith("https://www.booking.com/hotel"):
            return item["link"]

    return ""
