from typing import List
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import ConnectionError

from constants.constants import COMMON_HEADERS
from utils.utils_functions import log_with_timestamp


def get_page_content(url, headers=COMMON_HEADERS, verify=False) -> "BeautifulSoup":
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
        return BeautifulSoup(req.content, "html.parser")
    except ConnectionError:
        log_with_timestamp(
            f"The URL = {url} is not valid and the data cannot be fetched.",
            type="error",
        )
        return None


def find_content_on_page(content, element, attrs={}) -> List:
    """
    Finds elements with defined attrs in page content - parses HTML payload
    :param content: BeautifulSoup object with the HTML page content
    :param element: HTML element to parse
    :param attrs: additional params that define parsing - id, class, other attrs
    :return: List of pattern ocurrences
    """
    return content.find_all(element, attrs) if content else None


def _get_page_elements(element_list, index=None):
    if index is not None:
        if len(element_list) < index:
            raise ValueError("Element list doesn't contain index you requested!")
        return element_list[index]
    return element_list


def get_elements_on_page(**kwargs):
    content = find_content_on_page(
        kwargs["content"], kwargs["element"], kwargs["attrs"]
    )
    return _get_page_elements(content, kwargs["index"])


def _fetch_data_from_the_api(url):
    if url is None:
        return None
    response = get(url, headers=COMMON_HEADERS, verify=False)
    # TODO: if 404, log that
    if response.status_code == 200:
        return response.content
    log_with_timestamp(
        f"An error occurred while fetching the data from the URL = {url}", "error"
    )
    return None
