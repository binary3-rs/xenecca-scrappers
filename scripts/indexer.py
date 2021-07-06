from dao.course_dao import CourseDAO
from dao.learning_resource import LearningResourceDAO
from utils.elastic_indexing import store_obj_in_es_index

course_dao = CourseDAO()
learning_resource_dao = LearningResourceDAO()

for course in course_dao.find_all():
    print(f"Indexing course with the id = {course.id}")
    store_obj_in_es_index(course)

for learning_resource in learning_resource_dao.find_all():
    print(f"Indexing learning_resource with the id = {learning_resource.id}")
    store_obj_in_es_index(learning_resource)



