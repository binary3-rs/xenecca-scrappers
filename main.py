from controllers.coupon_scrapper import ScrapperRunner
import urllib3
from datetime import datetime
from utils.utils_functions import log, log_exception, log_with_timestamp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
if __name__ == "__main__":
    runner = ScrapperRunner()
    log(f"-----------Scrape results for the date: {datetime.utcnow()})-----------")
    page_no = 1  # NOTE: for possible page-wise scrape
    try:
        num_of_scrapped_courses = runner.scrape_all_on_smartybro_page(page_no)
        log_with_timestamp(f"{num_of_scrapped_courses} new courses added.")
    except Exception as e:
        log_exception(e)
    # TODO: add scraping of courses provided by users
    log(f"-----------END-----------")