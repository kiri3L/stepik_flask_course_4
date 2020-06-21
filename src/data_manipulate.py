import json

from src.data import teachers
from src.data import days_of_the_week

booking_file = "src/json/booking.json"
request_file = "src/json/request.json"
teachers_file = "src/json/teachers.json"


def save(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)


def load(filename):
    with open(filename) as f:
        return json.load(f)


def get_teachers():
    return load(teachers_file)


def filter_teachers_by_goal(goal, teachers):
    teachers_ = [t for t in teachers if goal in t["goals"]]
    return teachers_


def get_teacher(id, teachers):
    teacher = [t for t in teachers if t["id"] == id]
    if len(teacher) == 1:
        return teacher[0]
    return None


def update_request(client_name, client_phone, goal, time):
    data = load(request_file)
    data.append({"client": client_name, "phone": client_phone, "goal": goal, "time": time})
    save(request_file, data)


def update_booking(client_name, client_phone, day, time, teacher_id):
    if day not in days_of_the_week:
        return False
    teachers = get_teachers()
    teacher = get_teacher(teacher_id, teachers)
    if teacher is None:
        return False
    if not teacher["free"][day][time]:
        return False
    teacher["free"][day][time] = False
    save(teachers_file, teachers)
    data = load(booking_file)
    data.append({"client": client_name, "phone": client_phone, "teacher": teacher_id, "day": day, "time": time})
    save(booking_file, data)
    return True


if __name__ == "__main__":
    save(teachers_file, teachers)
    save(booking_file, [])
    save(request_file, [])
