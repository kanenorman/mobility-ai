import datetime
from typing import Dict, Union

from pymbta3 import Schedules

from config import configs


def get_schedules(
    route: Union[str, None] = None,
    min_time: Union[datetime.date, None] = None,
    max_time: Union[datetime.date, None] = None,
) -> Dict:
    schedules = Schedules(configs.MBTA_API_KEY)

    return schedules.get(route, min_time=min_time, max_time=max_time)
