from datetime import datetime

from constants.constants import NUM_OF_CONSEC_DAYS
from dao.category_dao import CategoryDAO
from dao.course_coupon_dao import CourseCouponDAO
from dao.course_dao import CourseDAO
from dao.curriculum_item_dao import CurriculumItemDAO
from dao.instructor_dao import InstructorDAO
from dao.language_dao import LanguageDAO
from dao.subcategory_dao import SubcategoryDAO
from dao.topic_dao import TopicDAO
from scrappers.smartybro_scrapper import SmartyBroScrapper
from scrappers.udemy_scrapper import UdemyScrapper
from utils.search import store_course_in_es_index
from utils.utils_functions import (download_image, load_data_into_dict, log,
                                   log_exception, log_with_timestamp,
                                   put_if_not_null, try_save)


class ScrapperRunner:
    def __init__(self):
        self.language_dao = LanguageDAO()
        self.category_dao = CategoryDAO()
        self.subcategory_dao = SubcategoryDAO()
        self.topic_dao = TopicDAO()
        self.instructor_dao = InstructorDAO()
        self.curriculum_item_dao = CurriculumItemDAO()
        self.course_dao = CourseDAO()
        self.coupon_dao = CourseCouponDAO()
        # cache
        self._courses = load_data_into_dict(self.course_dao, "udemy_url")
        self._languages = load_data_into_dict(self.language_dao, "name")
        self._categories = load_data_into_dict(self.category_dao, "name")
        self._subcategories = load_data_into_dict(self.subcategory_dao, "name")
        self._topics = load_data_into_dict(self.topic_dao, "name")
        self._instructors = load_data_into_dict(self.instructor_dao, "udemy_id")
        self._curriculum = _load_curriculum(self.curriculum_item_dao)
        self.smartybro_scrapper = SmartyBroScrapper()
        self.udemy_scrapper = UdemyScrapper()

    def scrape_all_on_smartybro_page(self, page_no):
        courses = self.smartybro_scrapper.find_host_and_udemy_urls_for_page(page_no)
        # do not scrape courses that're already scrapped
        courses_to_scrape = [
            (title, data)
            for title, data in courses.items()
            if data["udemy_url"] not in self._courses
        ]
        courses_to_scrape.sort(reverse=True)
        return self.scrape_courses_on_udemy(courses_to_scrape)

    def scrape_courses_on_udemy(self, courses):
        num_of_new_courses = 0
        for course, data in courses:
            udemy_url = data["udemy_url"]
            log_with_timestamp(
                f"<<< Fetching the details about the course with title = {course} >>>"
            )
            page_content = self.udemy_scrapper.get_page_content(udemy_url)
            if page_content is None:
                log_with_timestamp(
                    f"WARNING: Cannot fetch the data from the Udemy for the course with native"
                    f" url={udemy_url}",
                    "error",
                )
                continue
            udemy_id = self.udemy_scrapper.find_udemy_course_id(page_content)
            headline = self.udemy_scrapper.find_udemy_course_headline(page_content)
            if headline:
                headline = headline.strip()
            course = self._courses.get(udemy_url)
            # convert to constant -> 2 to constant
            course_is_new_or_updated = (
                True
                if course is None
                else (datetime.utcnow() - course.updated_at).days > NUM_OF_CONSEC_DAYS
            )
            if course_is_new_or_updated:
                course_details = self.udemy_scrapper.find_course_details(udemy_id)

                # get details needed for creating/finding objects
                language_name = course_details.get("basic_data", {}).get("language")
                category_name = course_details.get("basic_data", {}).get("category")
                subcategory_name = course_details.get("basic_data", {}).get(
                    "subcategory"
                )
                topic_name = course_details.get("basic_data", {}).get("topic")
                instructors_details = course_details.get("instructors", {})

                language = self._languages.get(language_name)
                category = self._categories.get(category_name)
                subcategory = self._subcategories.get(subcategory_name)
                topic = self._topics.get(topic_name)

                # TODO:
                if language is None:
                    language = self._try_save_language(language_name)
                    put_if_not_null(self._languages, language_name, language)
                if category is None:
                    category = self._try_save_category(category_name)
                    put_if_not_null(self._categories, category_name, category)

                if subcategory is None:
                    subcategory = self._try_save_subcategory(subcategory_name, category)
                    put_if_not_null(self._subcategories, subcategory_name, subcategory)
                if topic is None:
                    topic = self._try_save_topic(topic_name, subcategory)
                    put_if_not_null(self._topics, topic_name, topic)
                instructors = []
                for instructor_data in instructors_details:
                    instructor = self._instructors.get(instructor_data["udemy_id"])
                    if instructor is None:
                        instructor = self._try_save_instructor(instructor_data)
                        if instructor is not None:
                            instructors.append(instructor)
                            self._instructors[instructor.udemy_id] = instructor

                incentives = course_details["incentives"]
                headline_data = {
                    **course_details["headline_data"],
                    "headline": headline,
                }
                price_details = course_details["price_details"]
                ratings = {
                    f"rating_count_{key}": value
                    for key, value in course_details["ratings"].items()
                }
                to_update = course is not None

                # if not (category and subcategory and topic and language):
                #     continue
                course = self._try_save_course(
                    course,
                    **{
                        **incentives,
                        **headline_data,
                        **price_details,
                        **ratings,
                        **data,
                        "udemy_id": udemy_id,
                    },
                )
                if course is not None:
                    course.category = category
                    course.subcategory = subcategory
                    course.language = language
                    course.topic = topic
                    course.instructors = instructors
                    try:
                        self.course_dao.update()
                        store_course_in_es_index(course)
                    except Exception as e:
                        log_with_timestamp(f"FATAL ERROR: {e}", "error")
                        continue
                    if not to_update:
                        self._try_save_curriculum(
                            course_details["curriculum"], course.id
                        )
                    num_of_new_courses += 1
                    self._courses[course.udemy_url] = course

        return num_of_new_courses

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
        finally:
            return subcategory

    def _try_save_instructor(self, details):
        instructor = None
        try:
            image_url = details.get("original_image_url")
            instructor = self.instructor_dao.create(**details)
            image_path = None
            try:
                image_path = download_image(image_url, "instructor")
            except Exception as e:
                log(f"Instructor image cannot be fetched - reason: {e}", "error")

            instructor.image_path = image_path
            instructor = self.instructor_dao.save(instructor)
        except Exception as e:
            log_exception(e, "Instructor")
        finally:
            return instructor

    def _try_save_course(self, course=None, **data):
        try:
            if course is None:
                course = self.course_dao.create(**data)
            else:
                course = self.course_dao.update(course, **data)
            poster_url = data.get("original_poster_url")
            poster_filepath = None
            if poster_url is not None:
                try:
                    poster_filepath = download_image(poster_url)
                except Exception as e:
                    log(f"Course poster cannot be fetched - reason: {e}", "error")
            course.poster_path = poster_filepath
            # NOTE: will be persisted in course update
        except Exception as e:
            log_exception(e, "Course")
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

    def _try_save_topic(self, topic_name, subcategory):
        if topic_name is None or subcategory is None:
            return None
        topic = None
        try:
            topic = self.topic_dao.find_by_name(topic_name)
            if topic is None:
                topic = self.topic_dao.create(topic_name, subcategory)
        except Exception as e:
            log_exception(e, "Topic")
        finally:
            return topic

    def _try_save_curriculum(self, curriculum_details, course_id):
        for i in range(len(curriculum_details)):
            curriculum_details[i].update(**{"course_id": course_id})
        return try_save(
            self.curriculum_item_dao.create_in_batch,
            curriculum_details,
            [],
            "Curriculum item",
        )


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
