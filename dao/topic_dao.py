from database.models.topic import Topic
from database.sqlalchemy_extension import session


class TopicDAO:
    def __init__(self):
        self._session = session

    def find_all(self):
        return self._session.query(Topic).all()

    def find_by_name(self, name):
        return self._session.query(Topic).filter_by(name=name).first()

    def create(self, name, subcategory):
        return self.save(Topic(name, subcategory))

    def save(self, topic) -> "Topic":
        """Add topic to database"""
        try:
            self._session.add(topic)
            self._session.commit()
            return topic
        except Exception as e:
            self._session.rollback()
            raise e

    def delete(self, topic) -> None:
        """Deletes topic from the database."""
        self._session.delete(topic)
        self._session.commit()
