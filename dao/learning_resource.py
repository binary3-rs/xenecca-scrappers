from database.models.learning_resource import LearningResource
from database.sqlalchemy_extension import session


class LearningResourceDAO:
    def __init__(self):
        self._session = session

    def find_all(self):
        return self._session.query(LearningResource).all()

    def find_by_name(self, name):
        return self._session.query(LearningResource).filter_by(name=name)

    def create(self, **kwargs):
        return self.save(LearningResource(**kwargs))

    def save(self, resource) -> "LearningResource":
        """Add resource to database"""
        try:
            self._session.add(resource)
            self._session.commit()
            return resource
        except Exception as e:
            self._session.rollback()
            raise e

    def delete(self, resource) -> None:
        """Deletes resource from the database."""
        self._session.delete(resource)
        self._session.commit()
