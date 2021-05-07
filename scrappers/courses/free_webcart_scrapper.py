from re import compile, sub
from typing import List

from bs4 import BeautifulSoup

from constants.constants import FREEWEB_CART_BASE_URL
from scrappers import scrapper
from scrappers.scrapper import (
    find_content_on_page,
    get_page_content,
)


# public API
def find_course_details_on_page(page_no=1):
    url = f'{FREEWEB_CART_BASE_URL["prefix"]}{page_no}{FREEWEB_CART_BASE_URL["suffix"]}'
    page_content = _fetch_data_from_the_api(url)
    courses = find_host_urls_in_page_content(page_content)
    results = {}
    for course_title, host_url in courses.items():
        results[course_title] = {"host_url": host_url, **_find_course_details(host_url)}
        break
    return results


def find_host_urls_in_page_content(content) -> List:
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
        urls[title] = url
    return urls


# private
def _find_course_details(url):
    course_details_content = get_page_content(url)
    headline = _find_course_headline(course_details_content)
    category, subcategory = _find_course_category_and_subcategory(
        course_details_content
    )
    language = _find_course_language(course_details_content)
    poster_path = _find_course_poster(course_details_content)
    goals = _find_course_goals(course_details_content)
    description = _find_course_description(course_details_content)
    udemy_url = _find_course_udemy_url(course_details_content)
    return {
        "headline": headline,
        "category": category,
        "subcategory": subcategory,
        "language": language,
        "original_poster_url": poster_path,
        "goals": goals,
        "description": description,
        "udemy_url": udemy_url,
        "host_url": url,
    }


def _find_course_headline(content):
    headline_element = find_content_on_page(content, "div", "stm_lms_udemy_headline")
    headline = headline_element[0] if len(headline_element) > 0 else None
    if headline is not None:
        headline = headline.text.strip()
    return headline


def _find_course_udemy_url(content):
    buy_course_button = find_content_on_page(content, "div", "stm-lms-buy-buttons")
    udemy_url = buy_course_button[0].a["href"] if buy_course_button else None
    return udemy_url


def _find_course_category_and_subcategory(content):
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


def _find_course_description(content):
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
    clean_pattern = compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    for block in blocks:
        raw_content = "".join([str(subblock) for subblock in block])
        clean_text = sub(clean_pattern, "", raw_content)
        if (
            len(clean_text) == 0
            or "adsbygoogle" in clean_text
            or "function(v,d,o,ai)" in clean_text
        ):
            continue
        data.append(clean_text.strip())
    return data


def _find_course_goals(content):
    course_goals_element = find_content_on_page(
        content, "div", "stm_lms_course_objectives__single_text"
    )
    course_goals = []
    for goal in course_goals_element:
        goal_text = goal.text.strip()
        course_goals.append(goal_text)
    return [fr"<li>{goal}<\li>" for goal in course_goals]


def _find_course_poster(content):
    img_element = find_content_on_page(content, "div", "stm_lms_course__image")
    if len(img_element) > 0:
        try:
            return img_element[0].img.attrs.get("src", None)
        except AttributeError:
            return None
    return None


def _find_course_language(content):
    languages_element = find_content_on_page(
        content, "div", "stm_lms_udemy_caption_languages"
    )
    language = (
        languages_element[0].text.strip().split()[0] if languages_element else None
    )
    return language


def _fetch_data_from_the_api(url):
    data = scrapper.fetch_data_from_the_api(url)
    response = data.get("content")
    if response is None:
        return response
    return BeautifulSoup(response, features="html.parser")
