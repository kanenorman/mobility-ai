import datetime
from typing import Dict, Generator, Union

from pymbta3 import Schedules

from config import configs


def get_schedules(
    route: str,
    min_time: Union[datetime.date, None] = None,
    max_time: Union[datetime.date, None] = None,
) -> Generator[Dict, None, None]:
    """
    Get schedules from the MBTA API.

    Retrieves schedules for a specified route and time range using the MBTA API.

    Parameters:
    ----------
    route : str
        The route for which schedules are to be retrieved. Example "Red" for red line.
    min_time : Union[datetime.date, None], optional
        The minimum time for which schedules should be retrieved. If None, there is no lower bound on time.
    max_time : Union[datetime.date, None], optional
        The maximum time for which schedules should be retrieved. If None, there is no upper bound on time.

    Yields:
    ------
    Dict[str, Union[str, int]]
        A dictionary containing schedule data for the specified route and time range.
    """
    schedules = Schedules(configs.MBTA_API_KEY)
    yield from schedules.get(route=route, min_time=min_time, max_time=max_time)["data"]
