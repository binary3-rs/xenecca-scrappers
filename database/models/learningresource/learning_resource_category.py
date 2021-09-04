from datetime import datetime
from enum import Enum
from database.sqlalchemy_extension import *


class LearningResourceDomain(Enum):
    WEBDEV = 1
    MOBILE = 2
    DEVOPS = 3
    DSA = 4,
    SOFTWARE_DESIGN = 5
    DATASCIENCE = 6,
    DATABASES = 7,
    PROGRAMMING_LANGUAGES = 8,
    UI_AND_UX = 9
    COMPUTER_SCIENCE = 10
    DIGITAL_MARKETING = 11
    OTHER = 12


class LearningResourceCategory(Base):
    __tablename__ = "learning_resource_category"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    domain = db.Column(db.Enum(LearningResourceDomain))
    tags = db.Column(db.String(300), default="")
    logo = db.Column(db.String(300), default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
