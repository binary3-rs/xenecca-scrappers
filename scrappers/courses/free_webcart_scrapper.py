from re import compile, sub
from typing import Dict

from config.constants import (
    FREEWEB_CART_BASE_URL,
    COURSE_DESCRIPTION_LEN,
    COURSE_OBJECTIVES_LEN,
)
from scrappers.courses.base_course_scrapper import BaseCourseScrapper
from scrappers.scrapper import find_content_on_page, get_page_content
from utils.common import trim_to_len, udemy_url_to_slug


class FreeWebCartScrapper(BaseCourseScrapper):
    HOST_BASE_URL = FREEWEB_CART_BASE_URL

    @classmethod
    def find_host_urls_in_page_content(cls, content) -> Dict:
        """
        Finds elements with defined attrs in page content - parses HTML payload
        :param content: BeautifulSoup object with the HTML page content
        :return: List of pattern ocurrences
        """
        course_item_cards = find_content_on_page(
            content, "div", "stm_lms_courses__single__inner"
        )
        urls = {}
        for item in course_item_cards:
            title = item.h5.text
            url = item.a["href"]
            urls[title] = {"host_url": url}
        return urls

    @classmethod
    def _find_course_details(cls, url):
        course_details_content = get_page_content(url)
        headline = cls._find_course_headline(course_details_content)
        category, subcategory = cls._find_course_category_and_subcategory(
            course_details_content
        )
        language = cls._find_course_language(course_details_content)
        poster = cls._find_course_poster(course_details_content)
        objectives = cls._find_course_objectives(course_details_content)
        description = cls._find_course_description(course_details_content)
        udemy_url = cls._find_course_udemy_url(course_details_content)
        return {
            "headline": headline,
            "category": category,
            "subcategory": subcategory,
            "language": language,
            "original_poster_url": poster,
            "objectives": trim_to_len(objectives, COURSE_OBJECTIVES_LEN),
            "description": trim_to_len(description, COURSE_DESCRIPTION_LEN),
            "udemy_url": udemy_url,
            "host_url": url,
            "slug": udemy_url_to_slug(udemy_url)
        }

    def _find_course_url(cls, course_item):
        title_url_element = find_content_on_page(course_item, "h2", "grid-tit")[0]
        return title_url_element.text, title_url_element.a["href"]

    @classmethod
    def _find_course_udemy_url(cls, content):
        get_course_button = find_content_on_page(content, "div", "stm-lms-buy-buttons")
        if get_course_button is None:
            return None
        return get_course_button[0].a["href"]

    @classmethod
    def _find_course_category_and_subcategory(cls, content):
        navigations_elements = find_content_on_page(content, "div", "navxtBreads")
        items = (
            find_content_on_page(navigations_elements[0], "span")
            if len(navigations_elements) > 0
            else None
        )
        categories = []
        if len(items) >= 3:
            categories.append(items[2].text)
        if len(items) >= 5:
            categories.append(items[4].text)
        return categories

    @classmethod
    def _find_course_description(cls, content):
        description_element = find_content_on_page(
            content, "div", "stm_lms_course__content"
        )
        if len(description_element) == 0:
            return None
        description = description_element[0]
        blocks = find_content_on_page(
            description, ["div", "p", "h1", "h2", "h3", "h4", "h5", "h6", "strong"]
        )
        data = []
        for block in blocks:
            clean_text = clean_html_tags(block)
            if (
                    len(clean_text) == 0
                    or "adsbygoogle" in clean_text
                    or "function(v,d,o,ai)" in clean_text
            ):
                continue
            data.append(clean_text)
        return "\n".join(data)

    @classmethod
    def _find_course_headline(cls, content):
        headline_element = find_content_on_page(
            content, "div", "stm_lms_udemy_headline"
        )
        headline = headline_element[0] if len(headline_element) > 0 else None
        if headline is not None:
            headline = headline.text.strip()
        return headline

    @classmethod
    def _find_course_objectives(cls, content):
        course_goals_element = find_content_on_page(
            content, "div", "stm_lms_course_objectives__single_text"
        )
        course_goals = []
        for goal in course_goals_element:
            goal_text = goal.text.strip()
            course_goals.append(goal_text)
        return "".join([fr"<li>{goal}<\li>" for goal in course_goals])

    @classmethod
    def _find_course_language(cls, content):
        languages_element = find_content_on_page(
            content, "div", "stm_lms_udemy_caption_languages"
        )
        language = (
            languages_element[0].text.strip().split()[0] if languages_element else None
        )
        return language

    @classmethod
    def _find_course_poster(cls, content):
        img_element = find_content_on_page(content, "div", "stm_lms_course__image")
        if len(img_element) > 0:
            try:
                image_attrs = img_element[0].img.attrs
                img_src = image_attrs.get("src", None)
                if img_src is None or "data:image":
                    img_src = image_attrs.get("data-src", None)
                return img_src
            except AttributeError:
                return None
        return None


def clean_html_tags(block):
    clean_pattern = compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    raw_content = "".join([str(subblock.strip()) for subblock in block])
    text_with_mapped_tags = map_text_style_tags(raw_content)
    clean_text = sub(clean_pattern, "", text_with_mapped_tags).strip()
    return map_text_style_tags(clean_text, True)


def map_text_style_tags(text, reverse_mapping=False):
    text_style_map = {
        "<strong>": "--!!-STRONG-!!--",
        "</strong>": "--!!-ESTRONG-!!--",
        "<em>": "--!!-EM-!!--",
        "</em>": "--!!-EEM-!!--",
        "<b>": "--!!-B-!!--",
        "</b>": "--!!-EB-!!--",
        "<i>": "--!!-I-!!--",
        "</i>": "--!!-EI-!!--",
        "<u>": "--!!-U-!!--",
        "</u>": "--!!-EU-!!--",
        "<tt>": "--!!-TT-!!--",
        "</tt>": "--!!-ETT-!!--",
        "<big>": "--!!-BIG-!!--",
        "</big>": "--!!-EBIG-!!--",
        "<small>": "--!!-SMALL-!!--",
        "</small>": "--!!-ESMALL-!!--",
        "<sub>": "--!!-SUB-!!--",
        "</sub>": "--!!-ESUB-!!--",
        "<sup>": "--!!-SUP-!!--",
        "</sup>": "--!!-ESUP-!!--",
        "<br>": "--!!-BR-!!--",
        "</br>": "--!!-EBR-!!--",
        "<hr>": "--!!-HR-!!--",
        "</hr>": "--!!-EHR-!!--",
    }
    if reverse_mapping:
        char_map = {v: k for k, v in text_style_map.items()}
    else:
        char_map = text_style_map
    for element in char_map:
        text = text.replace(element, char_map.get(element, element))
    return text
