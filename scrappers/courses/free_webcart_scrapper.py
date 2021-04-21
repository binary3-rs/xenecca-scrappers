from typing import List

from scrappers.scrapper import find_content_on_page, get_page_content
from re import compile, sub


# public API
def find_host_links_in_page_content(content) -> List:
    """
    Finds elements with defined attrs in page content - parses HTML payload
    :param content: BeautifulSoup object with the HTML page content
    :return: List of pattern ocurrences
    """
    course_item_cards = find_content_on_page(content, "div", "stm_lms_courses__single")
    urls = {}
    for item in course_item_cards:
        title = item.h5.text
        url = item.a["href"]
        urls[title] = url
    return urls


def find_course_details(url):
    course_details_content = get_page_content(url)
    headline = _find_course_headline(course_details_content)
    category, subcategory = _find_course_category_and_subcategory(
        course_details_content
    )
    instructors = _find_course_instructors(course_details_content)
    num_of_students = _find_course_num_of_students(course_details_content)
    language = _find_course_language(course_details_content)
    rating = _find_course_rating(course_details_content)
    poster_path = _find_course_poster(course_details_content)
    goals = _find_course_goals(course_details_content)
    description = _find_course_description(course_details_content)
    incentives = _find_course_incentives(course_details_content)
    expiration_time = _find_course_expiration_time(course_details_content)
    reviews = _find_course_reviews(course_details_content)
    udemy_url = _find_course_udemy_url(course_details_content)
    return {
        "headline": headline,
        "category": category,
        "subcategory": subcategory,
        "instructors": instructors,
        "num_of_students": num_of_students,
        "language": language,
        "rating": rating,
        "poster": poster_path,
        "goals": goals,
        "description": description,
        "incentives": incentives,
        "expiration_time": expiration_time,
        "reviews": reviews,
        "udemy_url": udemy_url,
        "host_url": url,
    }


# private
def _find_course_headline(content):
    headline_element = find_content_on_page(content, "div", "stm_lms_udemy_headline")
    headline = headline_element[0] if len(headline_element) else None
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
        if len(navigations_elements)
        else None
    )
    categories = []
    if len(items) >= 3:
        categories.append(items[2].text)
    if len(items) >= 5:
        categories.append(items[4].text)
    return categories


def _find_course_expiration_time(content):
    expiration_time_element = find_content_on_page(
        content, "div", "stm_lms_expired_notice warning_expired"
    )
    expiration_time = (
        expiration_time_element[0].text.strip()
        if len(expiration_time_element)
        else None
    )
    return expiration_time


def _find_course_incentives(content):
    course_include_info_element = find_content_on_page(
        content, "div", "stm_lms_udemy_include heading_font"
    )
    include_items = {}
    for include_item in course_include_info_element:
        css_class = include_item.i.attrs["class"][0]
        text = include_item.text.strip()
        if "play" in css_class:
            include_items["duration"] = text
        elif "text-format" in css_class:
            include_items["num_of_articles"] = text
        elif "clock" in css_class:
            include_items["access_period"] = text
        elif "laptop-phone" in css_class:
            include_items["device_access"] = text
        elif "license2" in css_class:
            include_items["certificate"] = text
    return include_items


def _find_course_reviews(content):
    avg_rating_element = find_content_on_page(content, "div", "average_rating_value")
    if len(avg_rating_element):
        avg_rating = avg_rating_element[0].text
    num_of_ratings_element = find_content_on_page(content, "div", "average_rating_num")
    if len(num_of_ratings_element):
        num_of_ratings = num_of_ratings_element[0].text.split()[0]
    rating_values = [
        int(rating.text.strip())
        for rating in find_content_on_page(content, "td", "value")
    ]
    return {
        "avg_rating": avg_rating,
        "num_of_ratings": num_of_ratings,
        "rating_values": rating_values,
    }


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
        if "adsbygoogle" in clean_text:
            continue
        else:
            data.append(clean_text.strip())
            continue
    return data


def _find_course_goals(content):
    course_goals_element = find_content_on_page(
        content, "div", "stm_lms_course_objectives__single_text"
    )
    course_goals = []
    for goal in course_goals_element:
        goal_text = goal.text.strip()
        course_goals.append(goal_text)
    return [f"<li>{goal}<\li>" for goal in course_goals]


def _find_course_poster(content):
    img_element = find_content_on_page(content, "div", "stm_lms_course__image")
    if len(img_element):
        try:
            return img_element[0].img.attrs.get("src", None)
        except AttributeError:
            return None
    return None


def _find_course_rating(content):
    rating_element = find_content_on_page(
        content, "div", "average-rating-stars__av heading_font"
    )
    rating = rating_element[0].text.strip() if rating_element else None
    return rating


def _find_course_language(content):
    languages_element = find_content_on_page(
        content, "div", "stm_lms_udemy_caption_languages"
    )
    language = (
        languages_element[0].text.strip().split()[0] if languages_element else None
    )
    return language


def _find_course_num_of_students(content):
    students_enrolled_element = find_content_on_page(
        content, "div", "stm_lms_enrolled_num"
    )
    students_enrolled_line = (
        students_enrolled_element[0].text.strip() if students_enrolled_element else None
    )
    return students_enrolled_line.split()[0] if students_enrolled_line else None


def _find_course_instructors(content):
    instructor_element = find_content_on_page(
        content, "div", "meta-unit teacher clearfix"
    )
    if len(instructor_element):
        return [
            {
                "name": instructor_element[i].text.strip().split("Instructor:\n")[1],
                "image": instructor_element[i].img.attrs["src"],
            }
            for i in range(len(instructor_element))
        ]
    else:
        return None
