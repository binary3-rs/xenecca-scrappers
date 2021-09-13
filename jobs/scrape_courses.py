from datetime import datetime
import logging

import urllib3
from dotenv import load_dotenv

from controllers.coupon_scrapper import ScrapperRunner
from scrappers.course.free_webcart_scrapper import FreeWebCartScrapper
from scrappers.course.smartybro_scrapper import SmartyBroScrapper
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
    log("Phase #1: Scrapping courses....")
    total_courses_saved = 0
    for scrapper, args in scrappers:
        try:
            num_of_scrapped_courses, num_of_saved_courses = runner.scrape(scrapper, args)
            log_with_timestamp(f"{num_of_saved_courses} new courses added.")
            total_courses_saved += num_of_saved_courses
        except Exception as e:
            log_exception(e)
    log(f"Phase #2: Deleting oldest {total_courses_saved // 2} courses.....")
    try:
        runner.delete_first_k_courses(total_courses_saved // 2)
    except Exception as e:
        log_exception(e)
    log(f"-----------END-----------")
