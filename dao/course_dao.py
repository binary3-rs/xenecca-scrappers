from database.models.course import Course
from database.sqlalchemy_extension import session


class CourseDAO:
    def __init__(self):
        self._session = session

    def create(self, **kwargs):
        course = Course(**kwargs)
        return self.save(course)

    def find_by_title(self, title):
        return self._session.query(Course).filter_by(title=title).all()

    def find_by_udemy_url(self, udemy_url):
        return self._session.query(Course).filter_by(udemy_url=udemy_url).all()

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

    def save_all(self, courses) -> None:
        """Add course to database"""
        try:
            self._session.bulk_save_objects(courses)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e

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
