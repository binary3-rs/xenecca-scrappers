from datetime import datetime

from config.constants import NUM_OF_CONSEC_DAYS
from dao.category_dao import CategoryDAO
from dao.course_dao import CourseDAO

from dao.language_dao import LanguageDAO
from dao.subcategory_dao import SubcategoryDAO

from utils.file import delete_file
from utils.elastic_indexing import store_obj_in_es_index
from utils.common import (
    download_image,
    load_data_into_dict,
    log,
    log_exception,
    log_with_timestamp,
    put_if_not_null,
    try_save,
)


def load_cleaned_udemy_urls(dao):
    all_records = dao.find_all()
    return {item.udemy_url: item for item in all_records}


def load_course_slugs(dao):
    all_records = dao.find_all()
    return {item.slug: item for item in all_records}


class ScrapperRunner:
    def __init__(self):
        self.language_dao = LanguageDAO()
        self.category_dao = CategoryDAO()
        self.subcategory_dao = SubcategoryDAO()
        self.course_dao = CourseDAO()
        # cache
        self._courses = load_data_into_dict(self.course_dao, "title")
        self._languages = load_data_into_dict(self.language_dao, "name")
        self._categories = load_data_into_dict(self.category_dao, "name")
        self._subcategories = load_data_into_dict(self.subcategory_dao, "name")
        # self._course_urls = load_cleaned_udemy_urls(self.course_dao)
        self._slugs = load_course_slugs(self.course_dao)

    def scrape(self, scrapper, *arg):
        courses = scrapper.find_basic_courses_details(*arg)
        num_of_scrapped_courses = 0
        num_of_saved_courses = 0
        # do not scrape courses that're already scrapped
        courses_to_scrape = self._filter_present_courses(courses)
        courses_to_scrape.reverse()
        for course_data in courses_to_scrape:
            course_data = {
                **course_data,
                **scrapper.find_all_course_details(course_data.get("host_url")),
            }
            if course_data["slug"] in self._slugs:
                continue
            num_of_scrapped_courses += 1
            course = self._courses.get(course_data["title"])
            # NOTE: titles can vary on different websites for the same course
            course = self._save_scraped_data(course, course_data)
            num_of_saved_courses = num_of_saved_courses + (course is not None)
        return num_of_scrapped_courses, num_of_saved_courses

    def _save_scraped_data(self, course, course_data):
        course_is_new_or_updatable = self._is_new_or_non_recent_course(course)
        updated_course = None
        if not course_is_new_or_updatable:
            return updated_course

        poster_filepath = self.download_poster(course_data.get("original_poster_url"))
        course_data["poster_path"] = poster_filepath
        updated_course = self._save_course_data_to_db(course, course_data)
        if updated_course is not None:
            try:
                store_obj_in_es_index(updated_course)
                self.update_caches(updated_course)
            except Exception as e:
                log_with_timestamp(f"FATAL ERROR: {e}", "error")
        else:
            delete_file(course_data["poster_path"])
        return updated_course

    def _is_new_or_non_recent_course(self, course):
        return (
            True
            if course is None
            else (datetime.utcnow() - course.updated_at).days > NUM_OF_CONSEC_DAYS
        )

    def _save_course_data_to_db(self, course, course_data):
        category = get_or_save(
            self._categories,
            self._try_save_category,
            course_data.get("category"),
            **{"category_name": course_data.get("category")},
        )
        subcategory = get_or_save(
            self._subcategories,
            self._try_save_subcategory,
            course_data.get("subcategory"),
            **{
                "subcategory_name": course_data.get("subcategory"),
                "category": category,
            },
        )
        language = get_or_save(
            self._languages,
            self._try_save_language,
            course_data.get("language"),
            **{"language_name": course_data.get("language")},
        )
        course_data["category"] = category
        course_data["subcategory"] = subcategory
        course_data["language"] = language
        course = self._try_save_course(course, **course_data)
        return course

    def _filter_present_courses(self, courses):
        return [
            {"title": title, **data}
            for title, data in courses.items()
            if title not in self._courses
        ]

    # private fetching methods for communication with DAO
    def _try_save_subcategory(self, subcategory_name, category):
        if subcategory_name is None or category is None:
            return None
        subcategory = None
        try:
            subcategory = self.subcategory_dao.find_by_name(subcategory_name)
            if subcategory is None:
                subcategory = self.subcategory_dao.create(subcategory_name, category)
        except Exception as e:
            log_exception(e, "Subcategory")
            raise e
        finally:
            return subcategory

    def download_poster(self, poster_url):
        poster_filepath = None
        if poster_url is not None:
            try:
                poster_filepath = download_image(poster_url)
            except Exception as e:
                log(f"Course poster cannot be fetched - reason: {e}", "error")
        return poster_filepath

    def _create_course(self, course=None, **data):
        course = self.course_dao.create(**data)
        poster_url = data.get("original_poster_url")
        poster_filepath = None
        if poster_url is not None:
            try:
                poster_filepath = download_image(poster_url)
            except Exception as e:
                log(f"Course poster cannot be fetched - reason: {e}", "error")
        course.poster_path = poster_filepath
        self.course_dao.update()
        return course

    def _try_save_course(self, course=None, **data):
        try:
            if course is None:
                course = self.course_dao.create(**data)
            else:
                course = self.course_dao.update(course, **data)
        except Exception as e:
            log_exception(e, "Course")
            course = None
        finally:
            return course

    def _try_save_language(self, language_name):
        if language_name is not None:
            return try_save(self.language_dao.create, language_name, None, "Language")
        return None

    def _try_save_category(self, category_name):
        category = None
        if category_name is not None:
            return try_save(self.category_dao.create, category_name, None, "Category")
        return category

    def update_caches(self, course):
        put_if_not_null(self._courses, course.title if course else None, course)
        put_if_not_null(self._slugs, course.slug if course else None, course)
        #put_if_not_null(self._course_urls, course.udemy_url if course else None, course)
        put_if_not_null(
            self._languages,
            course.language.name if course.language else None,
            course.language,
        )
        put_if_not_null(
            self._categories,
            course.category.name if course.category else None,
            course.category,
        )
        put_if_not_null(
            self._subcategories,
            course.subcategory.name if course.subcategory else None,
            course.subcategory,
        )


def get_or_save(cache, persisting_function, key, **data):
    value = cache.get(key)
    if value is not None:
        return value
    return persisting_function(**data)


# helpers
def _load_curriculum(dao):
    all_records = dao.find_all()
    course_items = {}
    for item in all_records:
        course_id = item.course_id
        if course_id not in course_items:
            course_items[course_id] = []
        course_items[course_id].append(item)
    return course_items
