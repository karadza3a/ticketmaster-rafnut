import ticketpy
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(http_method_names=['GET'])
def test(request):
    tm_client = ticketpy.ApiClient('pm5ziloGTZxyxkn9iGiAXAuEaDAhgnJC')
    pages = tm_client.events.find(
        classification_name='Hip-Hop',
        state_code='GA',
        start_date_time='2017-12-01T20:00:00Z',
        end_date_time='2017-12-21T20:00:00Z'
    )

    ret = [[str(event) for event in page] for page in pages]
    return Response(ret)
