from ..sqlalchemy_extension import db, Base

course_instructor = db.Table('course_instructor', Base.metadata,
                             db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
                             db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.id'))
                             )

