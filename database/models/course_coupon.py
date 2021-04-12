from datetime import datetime

from ..sqlalchemy_extension import *


class CourseCoupon(Base):
    __tablename__ = "course_coupon"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.BigInteger, primary_key=True)
    course_url = db.Column(db.String, unique=True, nullable=False)
    coupon_code = db.Column(db.String(40))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)
    scrapped = db.Column(db.Boolean, default=False)
