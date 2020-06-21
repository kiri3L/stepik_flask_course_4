from src.app import db
# from sqlalchemy.dialects.postgresql import JSONB

teachers_goals_association = db.Table('teachers_goals',
                                      db.Column('teacher_id',
                                                db.Integer,
                                                db.ForeignKey('teachers.id')),
                                      db.Column('goal_key',
                                                db.String,
                                                db.ForeignKey('goals.key')))


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False, default='0')
    picture = db.Column(db.String, nullable=False, default='/static/default_picture/')
    price = db.Column(db.Integer, nullable=False)
    timetable = db.Column(db.JSON)

    goals = db.relationship('Goal',
                            secondary=teachers_goals_association,
                            back_populates='teachers')

    bookings = db.relationship('Booking', back_populates='teacher')


class Goal(db.Model):
    __tablename__ = 'goals'
    key = db.Column(db.String, primary_key=True)
    value = db.Column(db.String, unique=True, nullable=False)

    teachers = db.relationship('Teacher',
                               secondary=teachers_goals_association,
                               back_populates='goals')
    requests = db.relationship('Request', back_populates='goal')


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_phone = db.Column(db.String, nullable=False)
    client_name = db.Column(db.String, nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    day_of_the_week = db.Column(db.String, nullable=False)
    # CheckConstraint('day_of_the_week > 0 and day_of_the_week < 8')
    time_interval = db.Column(db.String, nullable=False)

    teacher = db.relationship('Teacher', back_populates='bookings')


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String, nullable=False)
    client_phone = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)

    goal_key = db.Column(db.String, db.ForeignKey('goals.key'))
    goal = db.relationship('Goal', back_populates='requests')

