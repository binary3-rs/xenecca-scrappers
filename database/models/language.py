from datetime import datetime
from typing import Dict

from ..sqlalchemy_extension import *
from ..sqlalchemy_extension import db


class Language(Base):
    __tablename__ = "language"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name
