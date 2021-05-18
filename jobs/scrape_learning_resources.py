from os import path
from scrappers.learning_resources.drive_scrapper import DriveScrapper
import logging
from datetime import datetime

from utils.common import log_exception, log
from config.config import GOOGLE_DISK_DIR_ID
from config.constants import RESOURCES_LOCATION, RESOURCES_DIR_NAME

LOCAL_FILE_PATH = path.dirname(path.realpath("__file__"))
# logger
logging.basicConfig(
    filename=f"../logs/scrapper-logs/learning-resources/{str(datetime.utcnow().strftime('%Y_%m_%d'))}.log",
    level=logging.DEBUG,
)
if __name__ == "__main__":
    drive_scrapper = DriveScrapper()
    log(f"-----------Scrape results for the date: {datetime.utcnow()})-----------")
    try:
        drive_scrapper.scrape(GOOGLE_DISK_DIR_ID, RESOURCES_LOCATION, RESOURCES_DIR_NAME)
    except Exception as e:
        log_exception(e)
    log(f"-----------END-----------")

