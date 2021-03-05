from os import path
import logging
LOCAL_FILE_PATH = path.dirname(path.realpath('__file__'))
# logger

logging.basicConfig(filename='../xenecca-scrappers/logs/coupon_scrapper.log', level=logging.DEBUG)

# media folder
COURSES_MEDIA_DIR_PATH = 'images/courses/'
