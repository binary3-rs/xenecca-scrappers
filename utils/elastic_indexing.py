# elastic search methods
from json import dumps, loads

from requests import put

from config.config import COURSES_ES_ENDPOINT, LEARNING_RESOURCES_ES_ENDPOINT
from database.models.course import Course
from utils.common import log_with_timestamp


def store_obj_in_es_index(obj):
    if isinstance(obj, Course):
        record_type = "course"
        mapped_object = _map_course_object_to_es_record(obj)
    else:
        record_type = "learning_resource"
        mapped_object = _map_learning_resource_object_to_es_record(obj)
    _store_es_record(obj.id, mapped_object, record_type)


def _store_es_record(obj_id, record, record_type="course"):
    endpoint_url = COURSES_ES_ENDPOINT if record_type == "course" else LEARNING_RESOURCES_ES_ENDPOINT
    try:
        res = put(
            f"{endpoint_url}{obj_id}",
            dumps(record),
            headers={"Content-Type": "application/json"},
        )
        res = loads(res.content)
        if "error" in res:
            raise ValueError(res["error"])
    except Exception as e:
        log_with_timestamp(f"Creating a record failed. Error message = {e}.")


def _map_course_object_to_es_record(course):
    return {
        "_class": "com.xenecca.api.model.elastic.CourseDoc",
        "title": course.title,
        "doc_id": course.id,
        "headline": course.headline,
        "slug": course.slug,
        "category": course.category.id if course.category else None,
        "subcategory": course.subcategory.id if course.subcategory else None,
        "language": course.language.id if course.language else None,
        "poster": course.poster_path,
        "updated_at": course.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    }


def _map_learning_resource_object_to_es_record(learning_resource):
    return {
        "_class": "com.xenecca.api.model.elastic.LearningResourceDoc",
        "doc_id": learning_resource.id,
        "name": learning_resource.name,
        "resource": learning_resource.resource,
        "category": learning_resource.resource_category.id if learning_resource.resource_category else None,
        "material_type": learning_resource.material_type.name,
        "resource_type": learning_resource.resource_type.name.capitalize(),
        "updated_at": learning_resource.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    }
