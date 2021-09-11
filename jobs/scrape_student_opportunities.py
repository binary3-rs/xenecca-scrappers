from datetime import datetime
import logging

import urllib3
from dotenv import load_dotenv

from utils.common import log, log_exception, log_with_timestamp
from scrappers.studentopportunity.scholarship_track_scrapper import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
# logger
logging.basicConfig(
    filename=f"../logs/scrapper-logs/student-opportunities/{str(datetime.utcnow().strftime('%Y_%m_%d'))}.log",
    level=logging.DEBUG)

if __name__ == "__main__":
    try:
        log(f"-----------Scrape results for the date: {datetime.utcnow()})-----------")
        scholarship_scrapper = ScholarshipTrackScrapper()
        log("### Scrapping data from ScholarshipTrack ###")
        log("Phase 1: Deleting old scrape results....")
        scholarship_scrapper.delete_old_scrape_results()
        log("Phase 2: Scrapping new opportunities....")
        scholarship_scrapper.scrape()
        log(f"-----------END-----------")
    except Exception as e:
        log_exception(e)
