import requests
from config import configs

_BASE_URL = "https://api-v3.mbta.com"
_HEADERS = {"Accept": "text/event-stream", "X-API-Key": configs.MBTA_API_KEY}


def get_schedules(
    route: str,
):
    """
    Get schedules from the MBTA API.

    Retrieves schedules for a specified route and time range using the MBTA API.

    Parameters
    ----------
    route
        The route for which schedules are to be retrieved. Example "Red" for red line.
    """
    url = f"{_BASE_URL}/schedules"
    params = {"filter[route]": route}

    return requests.get(url, stream=True, headers=_HEADERS, params=params)
