from database.models.category import Category
from ..sqlalchemy_extension import *
from datetime import datetime


class Subcategory(Base):
    __tablename__ = "subcategory"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    # associated entities
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = relationship(
        Category,
        backref="subcategories",
        primaryjoin="Subcategory.category_id == Category.id",
    )

    def __init__(self, name, category=None):
        self.name = name
        self.category = category
