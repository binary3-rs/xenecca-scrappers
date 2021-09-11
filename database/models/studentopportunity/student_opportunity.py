from datetime import datetime
from enum import Enum

from database.sqlalchemy_extension import Base, db


class OpportunityType(Enum):
    SCHOLARSHIP = 1
    FELLOWSHIP = 2
    INTERNSHIP = 3
    EVENT = 4


class StudentOpportunity(Base):
    __tablename__ = "student_opportunity"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.String(32), primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    type = db.Column(db.Enum(OpportunityType))
    origin_url = db.Column(db.String(360), unique=True, nullable=False)
    source = db.Column(db.String(300), default=None, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def __str__(self):
        return f'StudentOpportunity(id={self.id}, ' \
               f' title={self.title}, ' \
               f'type={self.type}, ' \
               f'origin_url={self.origin_url}, ' \
               f'source={self.source}, ' \
               f'is_scrapped={self.is_scrapped}, ' \
               f'created_at={self.created_at}, ' \
               f'updated_at={self.updated_at})'
