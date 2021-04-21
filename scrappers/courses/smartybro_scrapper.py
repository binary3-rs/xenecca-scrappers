from json import loads
from typing import List

from constants.constants import (
    COURSE_DESCRIPTION_LEN,
    COURSE_GOALS_LEN,
    COURSE_REQUIREMENTS_LEN,
    SMARTY_BRO_BASE_URL,
)
from scrappers.scrapper import find_content_on_page, get_page_content
from utils.utils_functions import log

# public API
def find_host_and_udemy_urls_for_page(page):
    url = f"{SMARTY_BRO_BASE_URL}{page}"
    page_content = get_page_content(url)
    host_urls = find_host_urls_in_page_content(page_content)
    results = {}
    for course_title, smartybro_url in host_urls.items():
        content = get_page_content(smartybro_url)
        udemy_url = _find_course_udemy_url(content)
        whatyoulllearn = _find_course_objectives(content)
        requirements = _find_course_requirements(content)
        description = _find_course_description(content)

        poster = _find_course_poster(content)
        if udemy_url:
            results[course_title] = {
                "smartybro_url": smartybro_url,
                "udemy_url": udemy_url,
                "goals": whatyoulllearn,
                "requirements": requirements,
                "description": description,
                "original_poster_url": poster,
            }
    return results


def find_host_urls_in_page_content(content) -> List:
    """
    Finds elements with defined attrs in page content - parses HTML payload
    :param content: BeautifulSoup object with the HTML page content
    :return: List of pattern ocurrences
    """
    urls = {}
    if content is None:
        return urls
    target_elements = find_content_on_page(content, "h2", "grid-tit")
    for item in target_elements:
        title = item.text
        url = item.a["href"]
        urls[title] = url
    return urls


# private
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


def _find_course_objectives(content):
    target_elements = find_content_on_page(
        content,
        "div",
        "ud-component--course-landing-page-udlite" "--whatwillyoulearn",
    )
    if len(target_elements):
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
    if len(target_elements):
        requirements_element = target_elements[0]
        data = requirements_element.attrs["data-component-props"]
        requirements = loads(data)
        return "".join([f"<li>{item}</li>" for item in requirements["prerequisites"]])[
            :COURSE_REQUIREMENTS_LEN
        ]
    return None


def _find_course_description(content):
    target_elements = find_content_on_page(
        content, "div", "ud-component--course-landing-page-udlite--description"
    )
    if len(target_elements):
        description_element = target_elements[0]
        data = description_element.attrs["data-component-props"]
        description = loads(data).get("description")
        return (
            description[:COURSE_DESCRIPTION_LEN]
            if description is not None
            else description
        )
    return None


def _find_course_poster(content):
    poster_elements = find_content_on_page(
        content, "img", {"width": "480", "height": "270"}
    )
    poster = poster_elements[0].attrs["data-src"] if len(poster_elements) else None
    return poster
