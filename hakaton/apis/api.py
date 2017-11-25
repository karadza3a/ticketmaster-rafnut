from urllib import request
from urllib import parse
import json

ticketmaster_url = 'https://app.ticketmaster.com/discovery/v2/events.json?apikey=pm5ziloGTZxyxkn9iGiAXAuEaDAhgnJC'


def api_call(url, params=None):
    if params is not None:
        url += "&" + parse.urlencode(params)
    print(url)
    response = json.loads(request.urlopen(url).read())
    return response


def ticketmaster_api_call(params):
    print(ticketmaster_url)
    print(params)
    return api_call(ticketmaster_url, params)
