from constants.config import COURSES_MEDIA_DIR_PATH
from utils.utils_functions import download_image, log
from scrappers.base_scrapper import BaseScrapper
from typing import List
from json import loads

from constants.course_coupons import SMARTY_BRO_BASE_URL


class SmartyBroScrapper(BaseScrapper):
    def __init__(self):
        pass

    def find_host_and_udemy_urls_for_page(self, page):
        url = f'{SMARTY_BRO_BASE_URL}{page}'
        page_content = self.get_page_content(url)
        host_urls = self.find_host_urls_in_page_content(page_content)
        results = {}
        for course_title, smartybro_url in host_urls.items():
            content = self.get_page_content(smartybro_url)
            udemy_url = self.find_course_udemy_url(content)
            whatyoulllearn = self._find_course_objectives(content)
            requirements = self._find_course_requirements(content)
            description = self._find_course_description(content)
            poster = self._find_course_poster(content)
            if udemy_url:
                results[course_title] = {"smartybro_url": smartybro_url,
                                         "udemy_url": udemy_url,
                                         "whatyoulllearn": whatyoulllearn,
                                         "requirements": requirements,
                                         "description": description,
                                         "poster_url": poster
                                         }
        return results

    def find_host_urls_in_page_content(self, content) -> List:
        """
        Finds elements with defined attrs in page content - parses HTML payload
        :param content: BeautifulSoup object with the HTML page content
        :return: List of pattern ocurrences
        """
        urls = {}
        if content is None:
            return urls
        target_elements = super()._find_content_on_page(content, 'h2', 'grid-tit')
        for item in target_elements:
            title = item.text
            url = item.a['href']
            urls[title] = url
        return urls

    def find_course_udemy_url(self, content):
        url_elements = super()._find_content_on_page(content, 'a', 'fasc-button fasc-size-xlarge fasc-type-flat')
        url_element = url_elements[0]
        non_cleaned_url = url_element['href']
        log(f"Non-cleaned udemy URL = {non_cleaned_url}")
        cleaned_url = non_cleaned_url.split('&')[0]
        if 'couponCode' not in cleaned_url:
            cleaned_url = '&'.join(non_cleaned_url.split('&')[:2])
        if 'udemy.com' not in cleaned_url:
            log(f"Non-udemy URL detected = {cleaned_url}", "warn")
            return None
        return cleaned_url

    def _find_course_objectives(self, content):
        target_elements = super()._find_content_on_page(content, 'div', 'ud-component--course-landing-page-udlite'
                                                                        '--whatwillyoulearn')
        if len(target_elements):
            objectives = target_elements[0]
            objectives_goals = objectives.attrs['data-component-props']
            objectives_data = loads(objectives_goals)
            return "".join([f'<li>{objective}</li>' for objective in list(objectives_data.values())[0]])
        return None

    def _find_course_requirements(self, content):
        target_elements = super()._find_content_on_page(content, 'div',
                                                        'ud-component--course-landing-page-udlite--requirements')
        if len(target_elements):
            requirements_element = target_elements[0]
            data = requirements_element.attrs['data-component-props']
            requirements = loads(data)
            return ''.join([f'<li>{item}</li>' for item in requirements['prerequisites']])
        return None

    def _find_course_description(self, content):
        target_elements = super()._find_content_on_page(content, 'div',
                                                        'ud-component--course-landing-page-udlite--description')
        if len(target_elements):
            description_element = target_elements[0]
            data = description_element.attrs['data-component-props']
            description = loads(data)
            return description.get('description')
        return None

    def _find_course_poster(self, content):
        poster_elements = super()._find_content_on_page(content, 'img', {'width': '480', 'height': '270'})
        poster = poster_elements[0].attrs['data-src']
        # if poster:
        #     download_image(poster, COURSES_MEDIA_DIR_PATH)
        return poster
