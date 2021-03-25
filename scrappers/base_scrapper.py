from typing import List

from requests.exceptions import ConnectionError
from requests import get
from bs4 import BeautifulSoup
from constants.constants import COMMON_HEADERS
from utils.utils_functions import log, log_with_timestamp


class BaseScrapper:
    def __init__(self):
        super().__init__()
        self.courses = {}

    def get_page_content(self, url, headers=COMMON_HEADERS, verify=False) -> 'BeautifulSoup':
        """
        Fetchs data content and returns content of the page as HTML payload
        :param url: target URL where to send request
        :param headers: HTTP headers
        :param verify: verification flag
        :return: BeautifulSoup object with the content of the page or None
        """
        try:
            req = get(url, headers=headers, verify=verify)
            log_with_timestamp(f"URL = {url}, data fetched successfully.", type="info")
            return BeautifulSoup(req.content, 'html.parser')
        except ConnectionError:
            log_with_timestamp(f"The URL = {url} is not valid and the data cannot be fetched.", type="error")
            return None

    def _find_content_on_page(self, content, element, attrs={}) -> List:
        """
        Finds elements with defined attrs in page content - parses HTML payload
        :param content: BeautifulSoup object with the HTML page content
        :param element: HTML element to parse
        :param attrs: additional params that define parsing - id, class, other attrs
        :return: List of pattern ocurrences
        """
        return content.find_all(element, attrs) if content else None

    def _fetch_data_from_the_api(self, url):
        if url is None:
            return None
        response = get(url, headers=COMMON_HEADERS, verify=False)
        # TODO: if 404, log that
        if response.status_code == 200:
            return response.content
        log_with_timestamp(f"An error occurred while fetching the data from the URL = {url}", "error")
        return None

    def find_course_details(self, url):
        pass

    def find_course_details_for_page(self, provider, page):
        pass

    def find_course_details_for_all_pages(self, provider):
        pass

    # def find_courses_from_all_pages(self, provider=LEARN_VIRAL):
    #     courses = {}
    #     page_no = 1
    #     num_of_consec_empty_pages = 0
    #     try:
    #         parsing_function = eval(f'apply_{provider["name"]}_url_scrapper')
    #     except NameError as e:
    #         print(e)
    #         raise Exception("Invalid website that provides course coupons!")
    #
    #     while True:
    #         urls_from_current_page = self.find_courses_links(provider, page_no, parsing_function)
    #         # print(urls_from_current_page)
    #         if not urls_from_current_page:
    #             num_of_consec_empty_pages = num_of_consec_empty_pages + 1
    #         else:
    #             scrapping_function = eval(f'parse_course_details_from_{provider["name"]}')
    #             courses_added = self.find_courses_details(urls_from_current_page, provider['headers'],
    #                                                       scrapping_function)
    #             if courses_added:
    #                 num_of_consec_empty_pages = 0
    #         if num_of_consec_empty_pages >= NUM_OF_CONSEC_EMPTY_PAGES_THRESHOLD or page_no > 1:
    #             break
    #         page_no = page_no + 1
    #     # print(self.courses)
    #     return courses
    #
    # def find_courses_links(self, provider, page, scrapping_function):
    #     try:
    #         base_url, headers, [element, attrs], need_original_content = provider['url'], provider['headers'], provider[
    #             'pattern_1st_level'], provider['need_original_content']
    #     except KeyError as e:
    #         raise Exception("Invalid website that provides course coupons!")
    #     url = base_url + str(page)
    #     # print(url)
    #     page_content = self.get_page_content(url, headers)
    #     content_for_parsing = self.find_in_page_content(page_content, element, **attrs)
    #     if need_original_content:
    #         return scrapping_function(content_for_parsing, page_content)
    #     return scrapping_function(content_for_parsing)
    #
    # def find_courses_details(self, urls, headers, scrapping_function):
    #     courses_added = False
    #     for title, url in urls.items():
    #         if title not in self.courses:
    #             # print(url)
    #             page_content = self.get_page_content(url, headers)
    #             course = scrapping_function(page_content)
    #             if course:
    #                 # TODO: save to db
    #                 self.courses[title] = course
    #                 courses_added = True
    #         # TODO: remove
    #         break
    #     return courses_added

    # def save_course(self, course):
    #     pass
    #
    # def save_courses(self, courses):
    #     for course in courses:
    #         self.save(course)
