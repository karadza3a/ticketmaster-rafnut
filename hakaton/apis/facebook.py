from rest_framework.decorators import api_view
from rest_framework.response import Response

from hakaton.apis import api


@api_view(http_method_names=['GET'])
def likes(request):
    access_token = request.GET['access_token']
    url = "https://graph.facebook.com/v2.11/me/music?"
    result = api.api_call(url, {"limit": "999", "access_token": access_token})

    url = "https://graph.facebook.com/v2.11/"
    artists = []
    for d in result['data']:
        res = api.api_call(url+d['id']+"?fields=picture", {"access_token": access_token})
        artists.append({"name": d['name'], "photo": res["picture"]["data"]["url"]})

    return Response(artists)

