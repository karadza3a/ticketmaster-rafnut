from hakaton.apis import ticketmaster
from hakaton.models import Plan
from datetime import datetime, timedelta
import json


time_format = "%Y-%m-%d"


def find_event(plan_id):
    plan_model = Plan.objects.get(id=plan_id)
    plan = json.loads(plan_model.plan_data)
    start_date = datetime.strptime(plan["event"]["date"], time_format) + timedelta(days=1)
    end_date = datetime.strptime(plan["end_date"], time_format) - timedelta(days=1)
    events = ticketmaster.upsell_event_helper(start_date.strftime(time_format),
                                              end_date.strftime(time_format),
                                              plan["hotel"]["lat"],
                                              plan["hotel"]["lon"])

    return events
