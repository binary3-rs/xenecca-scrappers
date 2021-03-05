from database.models.course import Course
from database.sqlalchemy_extension import db, session


# finish
class CourseDAO:
    def __init__(self):
        self._session = session

    # def find_by_name(self, name):
    #     return self._session.query(Category).filter_by(name=name)

    def create(self, **kwargs):
        course = Course(**kwargs)
        return self.save(course)

    def update(self, course=None, **kwargs):
        try:
            if course is not None:
                course = course.update(**kwargs)
            self._session.commit()
            return course
        except Exception as e:
            self._session.rollback()
            raise e

    def find_all(self):
        return self._session.query(Course).all()

    def save(self, course) -> "Course":
        """Add course to database"""
        try:
            self._session.add(course)
            self._session.commit()
            return course
        except Exception as e:
            self._session.rollback()
            raise e

    def delete(self, course) -> None:
        """Deletes course from the database."""
        self._session.delete(course)
        self._session.commit()
