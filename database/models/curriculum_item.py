from ..sqlalchemy_extension import db, Base, relationship
from datetime import datetime


class CurriculumItem(Base):
    __tablename__ = "curriculum_item"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.BigInteger, primary_key=True)
    udemy_lesson_id = db.Column(db.BigInteger, unique=True, nullable=True, default=None)
    title = db.Column(db.String(255), nullable=False)
    item_type = db.Column(db.String(20))  # TODO: change to enum
    index = db.Column(db.Integer, default=1)  # check if it is non-negative
    section_index = db.Column(db.Integer, default=0)  # check if it is non-negative
    content_length = db.Column(db.Integer, default=0)  # check if it is non-negative
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    course = relationship(
        "Course",
        backref="curriculum_items",
        primaryjoin="CurriculumItem.course_id == Course.id",
    )

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            print(key, value)
            if hasattr(self, key):
                setattr(self, key, value)
