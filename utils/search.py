# elastic search methods
from json import dumps, loads

from requests import put

from constants.constants import COURSES_ES_ENDPOINT
from utils.common import log_with_timestamp


def store_course_in_es_index(course):
    record = _convert_course_object_to_es_record(course)
    _store_course_es_record(course.id, record)


def _store_course_es_record(id, record):
    try:
        res = put(
            f"{COURSES_ES_ENDPOINT}{id}",
            dumps(record),
            headers={"Content-Type": "application/json"},
        )
        res = loads(res.content)
        if "error" in res:
            raise ValueError(res["error"])
    except Exception as e:
        log_with_timestamp(f"Creating a record failed. Error message = {e}.")


def _convert_course_object_to_es_record(course):
    return {
        "_class": "com.xenecca.api.es.models.CourseDoc",
        "title": course.title,
        "doc_id": course.id,
        "headline": course.headline,
        "category": course.category.id if course.category else None,
        "subcategory": course.subcategory.id if course.subcategory else None,
        "language": course.language.id if course.language else None,
        "poster": course.poster_path,
        "original_poster_url": course.original_poster_url,
        "updated_at": course.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    }
