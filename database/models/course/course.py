from datetime import datetime

from database.models.course.category import Category
from database.models.course.subcategory import Subcategory

from database.sqlalchemy_extension import Base, db, relationship
from .language import Language


class Course(Base):
    __tablename__ = "course"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.Text(6000))
    objectives = db.Column(db.Text(1000))
    headline = db.Column(db.String(255))
    poster_path = db.Column(db.String)
    original_poster_url = db.Column(db.String)
    requirements = db.Column(db.Text(1000))
    host_url = db.Column(db.String(300), unique=True, nullable=False)
    published_on_discord = db.Column(db.Boolean, default=False)
    slug = db.Column(db.String(350), unique=True, nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)
    udemy_url = db.Column(db.String(300), unique=True, nullable=False)

    # created_at = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())

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

    subcategory_id = db.Column(
        db.Integer, db.ForeignKey("subcategory.id"), nullable=False
    )
    subcategory = relationship(
        Subcategory,
        backref="courses",
        primaryjoin="Course.subcategory_id == Subcategory.id",
    )

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        # upon creation or change, we should republish this on Discord
        self.published_on_discord = False
        return self

    def __str__(self):
        return (
            f"Course: id = [{self.id}], title = [{self.title}], udemy_id = [{self.udemy_id}],"
            f" udemy_url = [{self.udemy_url}], smartybro_url = [{self.smartybro_url}]"
        )
