from datetime import datetime

import urllib3

from controllers.coupon_scrapper import ScrapperRunner
from scrappers.courses.free_webcart_scrapper import FreeWebCartScrapper
from scrappers.courses.smartybro_scrapper import SmartyBroScrapper
from utils.common import log, log_exception, log_with_timestamp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
if __name__ == "__main__":
    runner = ScrapperRunner()
    scrapper = FreeWebCartScrapper()
    log(f"-----------Scrape results for the date: {datetime.utcnow()})-----------")
    #page_no = 1  # NOTE: for possible page-wise scrape
    try:
        num_of_scrapped_courses, num_of_saved_courses = runner.scrape(scrapper)
        log_with_timestamp(f"{num_of_saved_courses} new courses added.")
    except Exception as e:
        log_exception(e)
    log(f"-----------END-----------")
