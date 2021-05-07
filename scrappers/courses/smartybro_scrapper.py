from json import loads
from typing import List

from constants.constants import (
    COURSE_DESCRIPTION_LEN,
    COURSE_GOALS_LEN,
    COURSE_REQUIREMENTS_LEN,
    HEADLINE_LEN,
    SMARTY_BRO_BASE_URL,
)
from scrappers.scrapper import find_content_on_page, get_page_content
from utils.category_and_topic_mapping import find_category_data
from utils.common import log


# public API
def find_course_details_on_page(page_no=1):
    url = f"{SMARTY_BRO_BASE_URL}{page_no}"
    page_content = get_page_content(url)
    courses = find_host_urls_and_categories_in_page_content(page_content)
    results = {}
    for course_title, data in courses.items():
        host_url = data["host_url"]
        results[course_title] = {**data, **_find_course_details(host_url)}
    return results


def find_host_urls_and_categories_in_page_content(content) -> List:
    """
    Finds elements with defined attrs in page content - parses HTML payload
    :param content: BeautifulSoup object with the HTML page content
    :return: List of pattern ocurrences
    """
    urls = {}
    course_urls_and_categories = {}
    if content is None:
        return urls
    course_items = find_content_on_page(content, "div", "post")
    for course_item in course_items:
        try:
            title, host_url = _find_course_url(course_item)
            category, subcategory = _find_course_category_and_subcategory(course_item)
            if category is None or subcategory is None:
                continue
            course_urls_and_categories[title] = {
                "host_url": host_url,
                "category": category,
                "subcategory": subcategory,
            }
        except (KeyError, IndexError, AttributeError):
            log("Course URL or categories cannot be extracted!", "error")
            continue
    return course_urls_and_categories


# private
def _find_course_details(url):
    content = get_page_content(url)
    udemy_url = _find_course_udemy_url(content)
    whatyoulllearn = _find_course_objectives(content)
    requirements = _find_course_requirements(content)
    description = _find_course_description(content)
    poster = _find_course_poster(content)
    if udemy_url is None:
        return {}
    return {
        "host_url": url,
        "udemy_url": udemy_url,
        "headline": _find_course_headline(description),
        "goals": whatyoulllearn,
        "requirements": requirements,
        "description": description,
        "original_poster_url": poster,
    }


def _find_course_url(course_item):
    title_url_element = find_content_on_page(course_item, "h2", "grid-tit")[0]
    return title_url_element.text, title_url_element.a["href"]


def _find_course_udemy_url(content):
    url_elements = find_content_on_page(
        content, "a", "fasc-button fasc-size-xlarge fasc-type-flat"
    )
    url_element = url_elements[0]
    non_cleaned_url = url_element["href"]
    log(f"Non-cleaned udemy URL = {non_cleaned_url}")
    cleaned_url = non_cleaned_url.split("&")[0]
    if "couponCode" not in cleaned_url:
        cleaned_url = "&".join(non_cleaned_url.split("&")[:2])
    if "udemy.com" not in cleaned_url:
        log(f"Non-udemy URL detected = {cleaned_url}", "warn")
        return None
    return cleaned_url.strip()


def _find_course_category_and_subcategory(content):
    category_elements = find_content_on_page(content, "span", "tag-post")
    categories = []
    for element in category_elements:
        categories.extend([category.strip() for category in element.text.split(",")])
    return find_category_data(categories)


def _find_course_description(content):
    target_elements = find_content_on_page(
        content, "div", "ud-component--course-landing-page-udlite--description"
    )
    if len(target_elements) > 0:
        description_element = target_elements[0]
        data = description_element.attrs["data-component-props"]
        description = loads(data).get("description")
        return (
            description[:COURSE_DESCRIPTION_LEN]
            if description is not None
            else description
        )
    return None


def _find_course_headline(description):
    return f"{description[:HEADLINE_LEN]}..." if description is not None else ""


def _find_course_objectives(content):
    target_elements = find_content_on_page(
        content,
        "div",
        "ud-component--course-landing-page-udlite" "--whatwillyoulearn",
    )
    if len(target_elements) > 0:
        objectives = target_elements[0]
        objectives_goals = objectives.attrs["data-component-props"]
        objectives_data = loads(objectives_goals)
        return "".join(
            [f"<li>{objective}</li>" for objective in list(objectives_data.values())[0]]
        )[:COURSE_GOALS_LEN]
    return None


def _find_course_requirements(content):
    target_elements = find_content_on_page(
        content, "div", "ud-component--course-landing-page-udlite--requirements"
    )
    if len(target_elements) > 0:
        requirements_element = target_elements[0]
        data = requirements_element.attrs["data-component-props"]
        requirements = loads(data)
        return "".join([f"<li>{item}</li>" for item in requirements["prerequisites"]])[
            :COURSE_REQUIREMENTS_LEN
        ]
    return None


def _find_course_poster(content):
    poster_elements = find_content_on_page(
        content, "img", {"width": "480", "height": "270"}
    )
    poster = poster_elements[0].attrs["data-src"] if len(poster_elements) > 0 else None
    return poster
