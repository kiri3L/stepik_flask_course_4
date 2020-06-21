from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, HiddenField
from wtforms.validators import InputRequired

from src.data import goals, time_per_week


class BookingForm(FlaskForm):
    name = StringField('Вас зовут', [InputRequired()])
    phone = StringField('Ваш телефон', [InputRequired()])
    hidden_day_of_the_week = HiddenField('day_of_the_week')
    hidden_time_interval = HiddenField('time_interval')
    hidden_teacher_id = HiddenField('teacher_id')


class RequestForm(FlaskForm):
    name = StringField('name', [InputRequired()])
    phone = StringField('phone', [InputRequired()])
    goals = RadioField('goals', choices=goals.items())
    time = RadioField('time', choices=time_per_week.items())
