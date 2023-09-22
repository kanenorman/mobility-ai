from typing import Dict, Union

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
def _make_api_request(endpoint: str, params: Union[Dict, None] = None):
    """
    Make an API request to the MBTA API.

    Parameters
    ----------
    endpoint
        The API endpoint to request (e.g., "schedules" or "alerts").
    params
        API request parameters

    Returns
    -------
    Generator
        A generator that yields bytes from the API response.
    """
    headers = {"Accept": "text/event-stream", "X-API-Key": configs.MBTA_API_KEY}
    url = f"https://api-v3.mbta.com/{endpoint}"

    with httpx.stream(
        method="GET",
        url=url,
        headers=headers,
        params=params,
        timeout=None,
    ) as stream:
        yield from stream.iter_bytes()


def get_schedules(params: Union[Dict, None] = None):
    """
    Get schedules from the MBTA API.

    A schedule is the arrival drop off and departure pick up time
    to/from a stop at a given sequence along a trip.

    Parameters
    ----------
    params
        API request parameters

    Notes
    -----
        A route, stop, or trip MUST be specified as a parameter.
        API docs: https://api-v3.mbta.com/docs/swagger/index.html#/Schedule
    """
    return _make_api_request("schedules", params)


def get_alerts(params: Union[Dict, None] = None):
    """
    Get alerts from the MBTA API.

    An alert is defined as an effect on a provided service, route, route_type,
    stop, and or trip. Described by a banner, short header, and image alternative
    text. It is caused by a cause that is somewhere in its lifecycle.

    Parameters
    ----------
    params
        API request parameters

    Notes
    -----
        API docs: https://api-v3.mbta.com/docs/swagger/index.html#/Alert
    """
    return _make_api_request("alerts", params)


def get_trips(params: Union[Dict, None] = None):
    """
    Get trips for the MBTA API.

    A Trip is defined as the journey of a particular vehicle
    through a set of stops on a primary route.

    Parameters
    ----------
    params
        API request parameters

    Notes
    -----
        A id, route, route_pattern, or name MUST be specified as a parameter.
        API docs: https://api-v3.mbta.com/docs/swagger/index.html#/Trip
    """
    return _make_api_request("trips", params)


def get_stops(params: Union[Dict, None] = None):
    """
    Get stops for the MBTA API.

    A stop is a location on a route that a vechicle stops to on/off load
    passengers.

    Parameters
    ----------
    params
        API request parameters

    Notes
    -----
        API docs: https://api-v3.mbta.com/docs/swagger/index.html#/Stop
    """
    return _make_api_request("stops", params)


def get_shapes(params: Union[Dict, None] = None):
    """
    Get shapes for the MBTA API.

    A shape is a geographic representaion of an object. (e.g. linestring, polygon).

    filter[route] MUST be specified for any shapes to be returned.

    Parameters
    ----------
    params
        API request parameters

    Notes
    -----
        API docs: https://api-v3.mbta.com/docs/swagger/index.html#/shapes
    """
    return _make_api_request("shapes", params)
