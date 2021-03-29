from sqlalchemy import CheckConstraint

from database.models.category import Category
from database.models.course_instructor import course_instructor
from database.models.curriculum_item import CurriculumItem
from database.models.subcategory import Subcategory
from database.models.topic import Topic
from ..sqlalchemy_extension import db, Base, relationship
from datetime import datetime

from .language import Language


class Course(Base):
    __tablename__ = "course"
    __table_args__ = (CheckConstraint('avg_rating >= 0 and avg_rating <= 5'), CheckConstraint('price >= 0'),
                      CheckConstraint('0 <= discount_percent <= 100'), CheckConstraint('0 <= duration_in_mins'),
                      CheckConstraint('num_of_articles >= 0'), CheckConstraint('num_of_reviews >= 0'),
                      CheckConstraint('students_enrolled >= 0'), CheckConstraint('rating_1 >= 0'),
                      CheckConstraint('rating_2 >= 0'), CheckConstraint('rating_3 >= 0'),
                      CheckConstraint('rating_4 >= 0'), CheckConstraint('rating_5 >= 0'))

    id = db.Column(db.BigInteger, primary_key=True)
    avg_rating = db.Column(db.Numeric(precision=6, scale=5))
    badge = db.Column(db.String(255))
    has_certificate = db.Column(db.Boolean)
    currency = db.Column(db.String(1))
    description = db.Column(db.Text(6000))
    devices_access = db.Column(db.String(40))
    discount_percent = db.Column(db.Integer, default=0)
    discount_period = db.Column(db.String(40))
    discount_code = db.Column(db.String(40))
    video_content_length = db.Column(db.String, default=0)
    goals = db.Column(db.Text(1000))
    headline = db.Column(db.String(255))
    poster_path = db.Column(db.String)
    is_coupon_active = db.Column(db.Boolean, default=True)
    is_archived = db.Column(db.Boolean, default=False)
    has_lifetime_access = db.Column(db.Boolean)
    num_of_articles = db.Column(db.Integer, default=1)
    num_of_reviews = db.Column(db.Integer, default=0)
    original_poster_url = db.Column(db.String)
    price = db.Column(db.Numeric(precision=6, scale=2), default=0)
    old_price = db.Column(db.Numeric(precision=6, scale=2), default=0)
    requirements = db.Column(db.Text(1000))
    smartybro_url = db.Column(db.String(300), unique=True, nullable=False)
    num_of_students = db.Column(db.Integer, default=0)
    title = db.Column(db.String(255), unique=True, nullable=False)
    udemy_id = db.Column(db.BigInteger, unique=True, nullable=False)
    udemy_url = db.Column(db.String(300), unique=True, nullable=False)

    # ratings
    rating_count_1 = db.Column(db.Integer, default=0)
    rating_count_2 = db.Column(db.Integer, default=0)
    rating_count_3 = db.Column(db.Integer, default=0)
    rating_count_4 = db.Column(db.Integer, default=0)
    rating_count_5 = db.Column(db.Integer, default=0)

    # created_at = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    #updated_at = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())

    # associated entities
    language_id = db.Column(db.Integer, db.ForeignKey("language.id"), nullable=False)
    language = relationship(
        Language,
        backref="courses",
        primaryjoin="Course.language_id == Language.id",
    )

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = relationship(
        Category,
        backref="courses",
        primaryjoin="Course.category_id == Category.id",
    )

    subcategory_id = db.Column(db.Integer, db.ForeignKey("subcategory.id"), nullable=False)
    subcategory = relationship(
        Subcategory,
        backref="courses",
        primaryjoin="Course.subcategory_id == Subcategory.id",
    )

    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=False)
    topic = relationship(
        Topic,
        backref="topics",
        primaryjoin="Course.topic_id == Topic.id",
    )

    instructors = relationship(
        "Instructor",
        secondary=course_instructor,
        backref="courses")

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.is_coupon_active = True
        return self

    def __str__(self):
        return f'Course: id = [{self.id}], title = [{self.title}], udemy_id = [{self.udemy_id}],' \
               f' udemy_url = [{self.udemy_url}], smartybro_url = [{self.smartybro_url}]'
