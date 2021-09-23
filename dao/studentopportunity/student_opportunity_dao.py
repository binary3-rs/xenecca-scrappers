from database.models.studentopportunity.student_opportunity import StudentOpportunity
from database.sqlalchemy_extension import session


class StudentOpportunityDao:
    def __init__(self):
        self._session = session

    def find_all(self):
        return self._session.query(StudentOpportunity).all()

    def find_by_title(self, title):
        return self._session.query(StudentOpportunity).filter_by(title=title)

    def create(self, name):
        return self.save(StudentOpportunity(name))

    def find_or_create(self, title):
        result = self._session.query(StudentOpportunity).filter_by(title=title).first()
        if result is None:
            student_opportunity = StudentOpportunity(title)
            result = self.save(student_opportunity)
        return result

    def delete_by_source(self, source_website):
        """Delete all student opportunities by source"""
        self._session.query(StudentOpportunity).filter(StudentOpportunity.source_website == source_website).delete()

    def save_all(self, opportunities) -> None:
        """Add student opportunities to database"""
        try:
            self._session.bulk_save_objects(opportunities)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e

    def save(self, student_opportunity) -> "StudentOpportunity":
        """Add student opportunity to database"""
        try:
            self._session.add(student_opportunity)
            self._session.commit()
            return student_opportunity
        except Exception as e:
            self._session.rollback()
            raise e

    def delete(self, student_opportunity) -> None:
        """Deletes student opportunity from the database."""
        self._session.delete(student_opportunity)
        self._session.commit()
