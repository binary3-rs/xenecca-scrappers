from sqlalchemy import CheckConstraint
from ..sqlalchemy_extension import db, Base
from datetime import datetime


class Instructor(Base):
    __tablename__ = "instructor"
    __table_args__ = (CheckConstraint('avg_rating >= 0 and avg_rating <= 5'), CheckConstraint('price >= 0'),
                      CheckConstraint('0 <= discount_percent <= 100'), CheckConstraint('0 <= duration_in_mins'),
                      CheckConstraint('num_of_articles >= 1'), CheckConstraint('num_of_reviews >= 0'),
                      CheckConstraint('students_enrolled >= 0'))

    id = db.Column(db.BigInteger, primary_key=True)
    avg_rating = db.Column(db.Numeric(precision=6, scale=5))
    bio = db.Column(db.Text(1500))
    image_path = db.Column(db.String)
    num_of_courses = db.Column(db.Integer, default=1)
    num_of_students = db.Column(db.Integer, default=0)
    original_image_url = db.Column(db.String)
    full_name = db.Column(db.String(100), unique=True, nullable=False)
    job_title = db.Column(db.String(150))
    udemy_id = db.Column(db.BigInteger, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
