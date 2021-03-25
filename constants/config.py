from os import path
import logging
from dotenv import load_dotenv

LOCAL_FILE_PATH = path.dirname(path.realpath('__file__'))
load_dotenv()
# logger
logging.basicConfig(filename='../xenecca-scrappers/logs/coupon_scrapper.log', level=logging.DEBUG)

# media folder
COURSES_MEDIA_DIR_PATH = 'images/courses/'

