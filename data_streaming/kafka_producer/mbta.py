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

    Retrieves schedules for a specified route.

    Parameters
    ----------
    params
        API request parameters
    """
    return _make_api_request("schedules", params)


def get_alerts(params: Union[Dict, None] = None):
    """
    Get alerts from the MBTA API.

    Retrieves alerts for a specified route.

    Parameters
    ----------
    params
        API request parameters
    """
    return _make_api_request("alerts", params)
