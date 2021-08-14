from dao.course_dao import CourseDAO
from re import split

course_dao = CourseDAO()
print("Starting with parsing course descriptions")
updated_courses = []
for course in course_dao.find_all():
    description = course.description
    if description is not None and description[0] == '{' and description[-1] == '}':
        description = "".join(split('\",|\"', description[1: -1]))
        description = ". ".join(description.split("."))
        course.description = description
        updated_courses.append(course)
course_dao.save_all(updated_courses)
print("Course descriptions have been successfully updated!")
