from database.models.curriculum_item import CurriculumItem
from database.sqlalchemy_extension import session


class CurriculumItemDAO:
    def __init__(self):
        self._session = session

    def find_all(self):
        return self._session.query(CurriculumItem).all()

    def find_by_course_id(self, course_id):
        return self._session.query(CurriculumItem).find_by(course_id=course_id)

    # def find_language_names(self):
    #     return self._session.query(Language.name).all()

    # def find_by_title(self, name):
    #     return self._session.query(Category).filter_by(name=name)
    #
    # def find_or_create(self, name):
    #     result = self._session.query(Category).filter_by(name=name).first()
    #     if result is None:
    #         category = Category(name)
    #         result = self.save(category)
    #     return result

    def create_without_save(self, **kwargs):
        curriculum_item = CurriculumItem(**kwargs)
        return curriculum_item

    def create_in_batch(self, data):
        try:
            self._session.bulk_insert_mappings(CurriculumItem, data)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e

    def save_in_batch(self, curriculum_items):
        self._session.bulk_save_objects(curriculum_items)
        self._session.commit()

    def save(self, curriculum_item) -> "CurriculumItem":
        """Add curriculum item to database"""
        self._session.add(curriculum_item)
        self._session.commit()
        return curriculum_item

    def _delete(self, curriculum_item) -> None:
        """Deletes curriculum item from the database."""
        self._session.delete(curriculum_item)
        self._session.commit()
