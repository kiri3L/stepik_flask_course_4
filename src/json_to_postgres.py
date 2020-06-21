import json

from src.models import *
from src.data import goals
from src.data_manipulate import load, \
                                teachers_file, \
                                booking_file, \
                                request_file

teachers = load(teachers_file)
bookings = load(booking_file)
requests = load(request_file)

for goal_key, goal_value in goals.items():
    g = Goal(key=goal_key, value=goal_value)
    db.session.add(g)
db.session.commit()

for teacher in teachers:
    t = Teacher(name=teacher['name'],
                about=teacher['about'],
                rating=teacher['rating'],
                picture=teacher['picture'],
                price=teacher['price'],
                timetable=json.dumps(teacher['free']))
    for goal in teacher['goals']:
        t.goals.append(Goal.query.filter(Goal.key == goal).first())
    db.session.add(t)
db.session.commit()


for booking in bookings:
    b = Booking(client_phone=booking['phone'],
                client_name=booking['client'],
                teacher_id=booking['teacher'],
                day_of_the_week=booking['day'],
                time_interval=booking['time'])
    db.session.add(b)
db.session.commit()

for request in requests:
    r = Request(client_name=requests['client'],
                client_phone=requests['phone'],
                time=requests['goal'],
                goal_key=requests['time'])
    db.session.add(r)
db.session.commit()



