import json

from flask import render_template, request, redirect
from src.app import app, db
from src.data import goals, days_of_the_week
from src.models import Teacher, Request, Booking, Goal
from src.forms import BookingForm, RequestForm


@app.route("/")
def render_main_page():
    teachers = Teacher.query.all()
    return render_template("index.html", teachers=teachers, goals=goals)


@app.route("/goal/<g>/")
def render_goal_page(g):
    goal = Goal.query.filter(Goal.key == g).first()
    if goal is None:
        pass
    teachers = goal.teachers
    return render_template("goal.html", teachers=teachers, goal=goals[g])


@app.route("/profile/<int:id>/")
def render_profile_page(id):
    teacher = Teacher.query.get_or_404(id)
    teacher.timetable = json.loads(teacher.timetable)
    goal = [g.value for g in teacher.goals]
    s = ', '.join(goal)
    return render_template("profile.html",
                           teacher=teacher,
                           goals=s,
                           days_of_the_week=days_of_the_week,
                           is_free=True)


@app.route('/request/', methods=['GET', 'POST'])
def render_request_page():
    form = RequestForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            args = {'client_name': form.name.data,
                    'client_phone': form.phone.data,
                    'time': form.time.data,
                    'goal_key': form.goals.data}
            r = Request(**args)
            db.session.add(r)
            db.session.commit()
            args['goal_key'] = goals[args['goal_key']]
            return render_template('request_done.html', **args)
    return render_template('request.html', goals=goals, form=form)


@app.route('/booking/<int:id>/<day>/<time>/', methods=['GET', 'POST'])
def render_booking_page(id, day, time):
    teacher = Teacher.query.get_or_404(id)
    args = {'id': id, 'day': day, 'time': time,
            'teacher': teacher,
            'days_of_the_week': days_of_the_week}
    if request.method == 'GET':
        form = BookingForm(hidden_day_of_the_week=day,
                           hidden_time_interval=time,
                           hidden_teacher_id=id)
        return render_template('booking.html', form=form, **args)
    else:
        form = BookingForm()
        if form.validate_on_submit():
            args = {'client_phone': form.phone.data,
                    'client_name': form.name.data,
                    'teacher_id': form.hidden_teacher_id.data,
                    'day_of_the_week': form.hidden_day_of_the_week.data,
                    'time_interval': form.hidden_time_interval.data}
            teacher = Teacher.query.get_or_404(args['teacher_id'])
            timetable = json.loads(teacher.timetable)
            if not timetable[args['day_of_the_week']][args['time_interval']]:
                pass
            timetable[args['day_of_the_week']][args['time_interval']] = False
            teacher.timetable = json.dumps(timetable)
            b = Booking(**args)
            db.session.add(b)
            db.session.add(teacher)
            db.session.commit()
            return render_template('booking_done.html', **args, picture=teacher.picture)
        return render_template('booking.html', form=form, **args)


