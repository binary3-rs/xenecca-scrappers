from datetime import datetime
from os import path
import logging

import urllib3
from dotenv import load_dotenv

from controllers.coupon_scrapper import ScrapperRunner
from scrappers.courses.free_webcart_scrapper import FreeWebCartScrapper
from scrappers.courses.smartybro_scrapper import SmartyBroScrapper
from utils.common import log, log_exception, log_with_timestamp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
# logger
logging.basicConfig(
    filename=f"../logs/scrapper-logs/courses/{str(datetime.utcnow().strftime('%Y_%m_%d'))}.log",
    level=logging.DEBUG,
)


if __name__ == "__main__":
    runner = ScrapperRunner()
    scrappers = [(SmartyBroScrapper(), (1,)), (FreeWebCartScrapper(), ("development", "it-software", "design"))]
    log(f"-----------Scrape results for the date: {datetime.utcnow()})-----------")
    for scrapper, args in scrappers:
        try:
            num_of_scrapped_courses, num_of_saved_courses = runner.scrape(scrapper, args)
            log_with_timestamp(f"{num_of_saved_courses} new courses added.")
        except Exception as e:
            log_exception(e)
    log(f"-----------END-----------")
