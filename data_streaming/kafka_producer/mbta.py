import httpx
from config import configs
from retry import retry


@retry(
    exceptions=(httpx.RequestError, httpx.HTTPError),
    delay=5,
    backoff=2,
    max_delay=60,
    tries=3,
)
def _make_api_request(endpoint: str, route: str):
    """
    Make an API request to the MBTA API.

    Parameters
    ----------
    endpoint
        The API endpoint to request (e.g., "schedules" or "alerts").
    route
        The route for which data is to be retrieved. Example "Red" for the red line.

    Returns
    -------
    Generator
        A generator that yields bytes from the API response.
    """
    headers = {"Accept": "text/event-stream", "X-API-Key": configs.MBTA_API_KEY}
    url = f"https://api-v3.mbta.com/{endpoint}"
    params = {"filter[route]": route}

    with httpx.stream(
        method="GET",
        url=url,
        headers=headers,
        params=params,
        timeout=None,
    ) as stream:
        yield from stream.iter_bytes()


def get_schedules(route: str):
    """
    Get schedules from the MBTA API.

    Retrieves schedules for a specified route.

    Parameters
    ----------
    route
        The route for which schedules are to be retrieved. Example "Red" for the red line.
    """
    return _make_api_request("schedules", route)


def get_alerts(route: str):
    """
    Get alerts from the MBTA API.

    Retrieves alerts for a specified route.

    Parameters
    ----------
    route
        The route for which alerts are to be retrieved. Example "Red" for the red line.
    """
    return _make_api_request("alerts", route)
