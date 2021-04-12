import logging
from datetime import datetime
from os import path

from dotenv import load_dotenv

LOCAL_FILE_PATH = path.dirname(path.realpath("__file__"))
load_dotenv()
# logger
logging.basicConfig(
    filename=f"../xenecca-scrappers/logs/coupon_scrapper_"
    f'{str(datetime.utcnow().strftime("%Y_%m_%d"))}.log',
    level=logging.DEBUG,
)

# media folder
COURSES_MEDIA_DIR_PATH = "images/courses/"
