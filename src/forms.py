from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField


class BookingForm(FlaskForm):
    name = StringField('name')
    phone = StringField('phone')
    hidden_day_of_the_week = StringField('day_of_the_week')
    hidden_time_interval = StringField('time_interval')
    hidden_teacher_id = IntegerField('teacher_id')


class RequestForm(FlaskForm):
    name = StringField('name')
    phone = StringField('phone')
    goal = StringField('goal')
    time = StringField('time')
