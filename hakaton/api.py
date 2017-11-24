from urllib import request
from urllib import parse
import json

url = 'https://app.ticketmaster.com/discovery/v2/events.json?apikey=pm5ziloGTZxyxkn9iGiAXAuEaDAhgnJC'


def get_events(params):
    full_url = url+"&"+parse.urlencode(params)
    print(full_url)
    response = json.loads(request.urlopen(full_url).read())
    return response
