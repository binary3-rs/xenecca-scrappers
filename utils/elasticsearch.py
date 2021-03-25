# elastic search methods
from constants.constants import COURSES_ES_ENDPOINT
from utils.utils_functions import log_with_timestamp
from json import loads, dumps
from requests import put


def store_course_in_es_index(course):
    id = course.id
    record = _convert_course_object_to_es_record(course)
    print(record)
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
        "_title": course.title,
        "_docId": course.id,
        "_headline": course.headline,
        "_price": course.price,
        "_avgRating": course.avg_rating,
        "_category": course.category.id,
        "_subcategory": course.subcategory.id,
        "_topic": course.topic.id,
        "_language": course.language.id,
        "_authors": [{'name': instructor.full_name} for instructor in course.instructors]
    }
