from database.models.instructor import Instructor
from database.sqlalchemy_extension import session


class InstructorDAO:
    def __init__(self):
        self._session = session

    def find_all(self):
        return self._session.query(Instructor).all()

    def find_by_udemy_id(self, udemy_id):
        return self._session.query(Instructor).filter_by(udemy_id=udemy_id).first()

    def find_by_full_name(self, full_name):
        return self._session.query(Instructor).filter_by(full_name=full_name).first()

    def find(self, udemy_id=None, full_name=None, **kwargs):
        instructor = None
        if udemy_id:
            instructor = self.find_by_udemy_id(udemy_id)
        elif full_name:
            instructor = self.find_by_full_name(full_name)
        return instructor

    def create(self, **kwargs):
        instructor = Instructor(**kwargs)
        return self.save(instructor)

    def save(self, instructor) -> "Instructor":
        """Add instructor to database"""
        try:
            self._session.add(instructor)
            self._session.commit()
            return instructor
        except Exception as e:
            self._session.rollback()
            raise e

    def delete(self, instructor) -> None:
        """Deletes instructor from the database."""
        self._session.delete(instructor)
        self._session.commit()
