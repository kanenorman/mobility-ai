import datetime
from typing import Dict, Generator, List, Union

import httpx
from config import configs
from pymbta3 import Schedules

_schedules = Schedules(configs.MBTA_API_KEY)
_base_url = "https://api-v3.mbta.com"


def get_schedules(
    route: str,
    min_time: Union[datetime.date, None] = None,
    max_time: Union[datetime.date, None] = None,
) -> Generator[Dict[str, Union[str, int]], None, None]:
    """
    Get schedules from the MBTA API.

    Retrieves schedules for a specified route and time range using the MBTA API.

    Parameters
    ----------
    route
        The route for which schedules are to be retrieved. Example "Red" for red line.
    min_time
        The minimum time for which schedules should be retrieved. If None, there is no lower bound on time.
    max_time
        The maximum time for which schedules should be retrieved. If None, there is no upper bound on time.

    Yields
    ------
    Dict[str, Union[str, int]]
        A dictionary containing schedule data for the specified route and time range.
    """
    yield from _schedules.get(route=route, min_time=min_time, max_time=max_time)["data"]


async def get_predictions(
    route: str, trip: str, stop: str
) -> List[Dict[str, Union[str, int]]]:
    """
    Get predictions from the MBTA API.

    Retrieves prediction data for a specified route, trip, and stop using the MBTA API.

    Parameters:
    ----------
    route
        The route for which predictions are to be retrieved.
    trip
        The trip identifier for which predictions are to be retrieved.
    stop
        The stop identifier for which predictions are to be retrieved.

    Returns:
    -------
    List[Dict[str, Union[str, int]]]
        A list of dictionaries containing prediction data for the specified route, trip, and stop.
    """
    url = f"{_base_url}/predictions"
    headers = {"X-API-Key": configs.MBTA_API_KEY}
    params = {"route": route, "trip": trip, "stop": stop}

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()["data"]
        else:
            return [{"error": "An error occurred"}]
