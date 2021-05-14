from database.models.learning_resource_category import LearningResourceCategory
from database.sqlalchemy_extension import session


class LearningResourceCategoryDAO:
    def __init__(self):
        self._session = session

    def find_all(self):
        return self._session.query(LearningResourceCategory).all()

    def find_by_name(self, name):
        return self._session.query(LearningResourceCategory).filter_by(name=name)

    def create(self, **kwargs):
        return self.save(LearningResourceCategory(**kwargs))

    def save(self, resource_category) -> "LearningResourceCategory":
        """Add resource category to database"""
        try:
            self._session.add(resource_category)
            self._session.commit()
            return resource_category
        except Exception as e:
            self._session.rollback()
            raise e

    def delete(self, resource_category) -> None:
        """Deletes resource category from the database."""
        self._session.delete(resource_category)
        self._session.commit()
