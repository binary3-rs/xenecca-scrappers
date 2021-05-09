from database.models.language import Language
from database.sqlalchemy_extension import session


class LanguageDAO:
    def __init__(self):
        self._session = session

    def find_all(self):
        return self._session.query(Language).all()

    def find_language_names(self):
        return self._session.query(Language.name).all()

    def find_by_name(self, name):
        return self._session.query(Language).filter_by(name=name)

    def create(self, name):
        return self.save(Language(name))

    def find_or_create(self, name):
        result = self._session.query(Language).filter_by(name=name).first()
        if result is None:
            language = Language(name)
            result = self.save(language)
        return result

    def save(self, language) -> "Language":
        """Add language to database"""
        try:
            self._session.add(language)
            self._session.commit()
            return language
        except Exception as e:
            self._session.rollback()
            raise e

    def delete(self, language) -> None:
        """Deletes language from the database."""
        self._session.delete(language)
        self._session.commit()
