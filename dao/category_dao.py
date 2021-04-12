from database.models.category import Category
from database.sqlalchemy_extension import db, session


class CategoryDAO:
    def __init__(self):
        self._session = session

    def find_all(self):
        return self._session.query(Category).all()

    def find_by_name(self, name):
        return self._session.query(Category).filter_by(name=name)

    def create(self, name):
        return self.save(Category(name))

    def find_or_create(self, name):
        result = self._session.query(Category).filter_by(name=name).first()
        if result is None:
            category = Category(name)
            result = self.save(category)
        return result

    def save(self, category) -> "Category":
        """Add category to database"""
        try:
            self._session.add(category)
            self._session.commit()
            return category
        except Exception as e:
            self._session.rollback()
            raise e

    def delete(self, category) -> None:
        """Deletes category from the database."""
        self._session.delete(category)
        self._session.commit()
