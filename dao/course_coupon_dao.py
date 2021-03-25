from database.models.course_coupon import CourseCoupon
from database.sqlalchemy_extension import db, session


class CourseCouponDAO:
    def __init__(self):
        self._session = session

    def find_by_state(self, approved=True, scrapped=False):
        return self._session.query(CourseCoupon).filter_by(approved=approved, scrapped=scrapped)

    def update(self, coupon=None, **kwargs):
        try:
            if coupon is not None:
                coupon = coupon.update(**kwargs)
            self._session.commit()
            return coupon
        except Exception as e:
            self._session.rollback()
            raise e

    def save(self, coupon) -> "CourseCoupon":
        """Add coupon to database"""
        try:
            self._session.add(coupon)
            self._session.commit()
            return coupon
        except Exception as e:
            self._session.rollback()
            raise e

    def delete(self, coupon) -> None:
        """Deletes coupon from the database."""
        self._session.delete(coupon)
        self._session.commit()
