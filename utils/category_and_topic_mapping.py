from os import path, sep

from utils.common import load_from_json
from constants.constants import CATEGORIES_JSON_PATH
PARENT_FILE_PATH = path.dirname(path.realpath("__file__"))

categories = load_from_json(f'{PARENT_FILE_PATH}{sep}{CATEGORIES_JSON_PATH}')


def find_category_data(data):
    subcategories = []
    for category in data:
        if category in categories:
            subcategories = categories.get(category)
            break
    if len(subcategories) == 0:
        return find_categories_by_technology(data)
    subcategories = set(subcategories)
    subcategory = "Other"
    for item in data:
        if item in subcategories:
            return category, item
    return category, subcategory


def find_categories_by_technology(data):
    # TODO: implement determination of the category/subcategory by technology
    return None, None


