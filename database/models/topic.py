from database.models.subcategory import Subcategory
from ..sqlalchemy_extension import *
from datetime import datetime


class Topic(Base):
    __tablename__ = "topic"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # associated entities
    subcategory_id = db.Column(db.Integer, db.ForeignKey("subcategory.id"), nullable=False)
    subcategory = relationship(
        Subcategory,
        backref="topics",
        primaryjoin="Topic.subcategory_id == Subcategory.id",
    )

    def __init__(self, name, subcategory):
        self.name = name
        self.subcategory = subcategory
