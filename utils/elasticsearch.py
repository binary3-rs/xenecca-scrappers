# elastic search methods
from constants.constants import COURSES_ES_ENDPOINT
from utils.utils_functions import log_with_timestamp
from json import loads, dumps
from requests import put


def store_course_in_es_index(course):
    id = course.id
    record = _convert_course_object_to_es_record(course)
    _store_course_es_record(id, record)


def _store_course_es_record(id, record):
    try:
        res = put(f'{COURSES_ES_ENDPOINT}{id}', dumps(record), headers={'Content-Type': 'application/json'})
        res = loads(res.content)
        if 'error' in res:
            raise ValueError(res['error'])
    except Exception as e:
        log_with_timestamp(f"Creating a record failed. Error message = {e}.")
        print(e)


def _convert_course_object_to_es_record(course):
    return {
        "_class": "com.xenecca.api.es.models.CourseDoc",
        "title": course.title,
        "doc_id": course.id,
        "headline": course.headline,
        "price": str(course.price),
        "price_as_string": str(course.price) + str(course.currency),
        "avg_rating": str(course.avg_rating),
        "category": course.category.id,
        "subcategory": course.subcategory.id,
        "topic": course.topic.id,
        "language": course.language.id,
        "image": course.image_path,
        "original_image_url": course.original_image_url,
        "students_enrolled": course.students_enrolled,
        "num_of_reviews": course.num_of_reviews,
        "discount_period": course.discount_period,
        "time_added": course.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        "authors": [{'name': instructor.full_name, "image": instructor.image_path} for instructor in course.instructors]
    }
