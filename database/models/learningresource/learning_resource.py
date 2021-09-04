from datetime import datetime

from database.models.learningresource.learning_resource_category import LearningResourceCategory
from database.sqlalchemy_extension import *
from enum import Enum


class MaterialType(Enum):
    URL = 1
    FILE = 2


class ResourceType(Enum):
    CHEATSHEET = 1
    BOOK = 2
    SCRIPT = 3
    IMAGE = 4
    BLOG_OR_ARTICLE = 5
    TUTORIAL_OR_COURSE = 6
    WEBSITE = 7
    PODCAST = 8
    COLLECTION = 9
    @classmethod
    def str_to_enum(cls, name):
        name_l = name.lower()
        for value in cls._value2member_map_.values():
            if value.name.lower() == name_l:
                return value
        raise ValueError(f"ResourceType({name}) is not valid!")


class LearningResource(Base):
    __tablename__ = "learning_resource"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    resource = db.Column(db.String(500), unique=True, nullable=False)
    material_type = db.Column(db.Enum(MaterialType))
    resource_type = db.Column(db.Enum(ResourceType))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    resource_category_id = db.Column(db.Integer, db.ForeignKey("learning_resource_category.id"), nullable=False)
    resource_category = relationship(
        LearningResourceCategory,
        backref="resources",
        primaryjoin="LearningResource.resource_category_id == LearningResourceCategory.id",
    )

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)