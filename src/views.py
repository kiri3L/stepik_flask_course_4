from flask import render_template, request
from src import app
from src.data import goals, days_of_the_week
from src.data_manipulate import get_teachers, filter_teachers_by_goal, get_teacher, update_request, update_booking


@app.route("/")
def render_main_page():
    teachers = get_teachers()
    return render_template("index.html", teachers=teachers, goals=goals)


@app.route("/goal/<g>/")
def render_goal_page(g):
    if g not in goals:
        return render_template('404_error_page.html'), 404
    teachers = filter_teachers_by_goal(g, get_teachers())
    return render_template("goal.html", teachers=teachers, goal=goals[g])


@app.route("/profile/<int:id>/")
def render_profile_page(id):
    teachers = get_teachers()
    teacher = get_teacher(id, teachers)
    if teacher is None:
        return render_template('404_error_page.html'), 404
    goal = [goals[g] for g in teacher["goals"]]
    s = ', '.join(goal)
    return render_template("profile.html", teacher=teacher, goals=s, days_of_the_week=days_of_the_week, is_free=True)


@app.route("/request/")
def render_request_page():
    return render_template("request.html", goals=goals)


@app.route("/request_done/", methods=["POST"])
def render_request_done_page():
    # сохранить данные в request.json

    name = request.form.get("name")
    phone = request.form.get("phone")
    goal = request.form.get("goal")
    goal_value = goals[goal]
    time = request.form.get("time")

    if goal not in goals:
        return render_template('404_error_page.html'), 404
    update_request(name, phone, goal, time)
    return render_template('request_done.html', goal=goal_value, time=time, name=name, phone=phone)


@app.route("/booking/<int:id>/<day>/<time>/")
def render_booking_page(id, day, time):
    teachers = get_teachers()
    teacher = get_teacher(id, teachers)
    if teacher is None:
        return render_template('404_error_page.html'), 404
    return render_template("booking.html", day=day, time=time, teacher=teacher, days_of_the_week=days_of_the_week)


@app.route("/booking_done/", methods=["POST"])
def render_booking_done_page():
    name = request.form.get("clientName")
    phone = request.form.get("clientPhone")
    day = request.form.get("clientWeekday")
    day_name = days_of_the_week[day]
    time = request.form.get("clientTime")
    id = int(request.form.get("clientTeacher"))

    if not update_booking(name, phone, day, time, id):
        return render_template('404_error_page.html'), 404
    teacher = get_teacher(id, get_teachers())
    return render_template('booking_done.html', time=time, day=day_name, name=name, phone=phone, pictuer=teacher["picture"])
