from database.models.subcategory import Subcategory
from database.sqlalchemy_extension import session


class SubcategoryDAO:
    def __init__(self):
        self._session = session

    def find_all(self):
        return self._session.query(Subcategory).all()

    def find_by_name(self, name):
        return self._session.query(Subcategory).filter_by(name=name).first()

    def create(self, name, category):
        return self.save(Subcategory(name, category))

    def save(self, subcategory) -> "Subcategory":
        """Add subcategory to database"""
        try:
            self._session.add(subcategory)
            self._session.commit()
            return subcategory
        except Exception as e:
            self._session.rollback()
            raise e

    def delete(self, subcategory) -> None:
        """Deletes subcategory from the database."""
        self._session.delete(subcategory)
        self._session.commit()
