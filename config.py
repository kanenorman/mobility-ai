import os

from dotenv import load_dotenv

load_dotenv()

configs = {
    "KAFKA_HOST": os.environ["KAFKA_HOST"],
    "KAFKA_PORT": os.environ["KAFKA_PORT"],
    "SCHEDULES_INPUT_TOPIC": os.environ["SCHEDULES_INPUT_TOPIC"],
    "MBTA_API_KEY": os.environ["MBTA_API_KEY"],
}
