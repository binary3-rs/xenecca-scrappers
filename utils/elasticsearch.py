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


def _convert_course_object_to_es_record(course):
    course_duration = course.video_content_length
    try:
        duration = float(course_duration.split()[0])
    except:
        duration = 0
    return {
        "_class": "com.xenecca.api.es.models.CourseDoc",
        "title": course.title,
        "doc_id": course.id,
        "badge": course.badge,
        "headline": course.headline,
        "price": float(course.price),
        "old_price": float(course.old_price),
        "price_as_string": str(course.price) + str(course.currency),
        "avg_rating": str(course.avg_rating),
        "category": course.category.id if course.category else None,
        "subcategory": course.subcategory.id if course.subcategory else None,
        "topic": course.topic.id if course.topic else None,
        "language": course.language.id if course.language else None,
        "poster": course.poster_path,
        "original_poster_url": course.original_poster_url,
        "duration_in_hrs": duration,
        "num_of_students": course.num_of_students,
        "num_of_reviews": course.num_of_reviews,
        "updated_at": course.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        "instructors": [{'full_name': instructor.full_name, "image": instructor.image_path} for instructor in
                        course.instructors]
    }
