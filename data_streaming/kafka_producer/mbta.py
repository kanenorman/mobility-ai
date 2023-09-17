import httpx
import retry
from config import configs

_BASE_URL = "https://api-v3.mbta.com"
_HEADERS = {"Accept": "text/event-stream", "X-API-Key": configs.MBTA_API_KEY}


@retry(httpx.RequestError, httpx.HTTPError, delay=5, backoff=2, max_delay=60, tries=3)
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

    with httpx.stream(
        method="GET",
        url=url,
        headers=_HEADERS,
        params=params,
        timeout=None,
    ) as stream:
        yield from stream.iter_bytes()
