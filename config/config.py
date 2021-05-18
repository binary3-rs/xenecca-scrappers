import logging
from datetime import datetime
from os import path, getenv

from dotenv import load_dotenv

LOCAL_FILE_PATH = path.dirname(path.realpath("__file__"))
load_dotenv()
# logger
logging.basicConfig(
    filename=f"../logs/scrapper-logs/coupon_scrapper_"
             f'{str(datetime.utcnow().strftime("%Y_%m_%d"))}.log',
    level=logging.DEBUG,
)

# elastic search data

ES_PORT = getenv("ES_PORT", 9200)
ES_COURSES_INDEX = getenv("ES_COURSES_INDEX", "xenecca-course")
COURSES_ES_ENDPOINT = f"http://localhost:{ES_PORT}/{ES_COURSES_INDEX}/_doc/"

ES_RESOURCES_INDEX = getenv("ES_RESOURSES_INDEX", "xenecca-learning-resource")
LEARNING_RESOURCES_ES_ENDPOINT = f"http://localhost:{ES_PORT}/{ES_RESOURCES_INDEX}/_doc/"

# media folder
COURSES_MEDIA_DIR_PATH = "images/courses/"

GOOGLE_DISK_DIR_ID = getenv("GOOGLE_DISK_DIR_ID")
