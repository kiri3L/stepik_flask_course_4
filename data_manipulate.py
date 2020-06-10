import json

from data import teachers
from data import days_of_the_week
from data import goals


def save(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)


def load(filename):
    with open(filename) as f:
        return json.load(f)


def get_teachers():
    return load("teachers.json")


def filter_teachers_by_goal(goal, teachers):
    teachers_ = [t for t in teachers if goal in t["goals"]]
    return teachers_


def get_teacher(id, teachers):
    teacher = [t for t in teachers if t["id"] == id]
    if len(teacher) == 1:
        return teacher[0]
    return None


def update_request(client_name, client_phone, goal, time):
    data = load("request.json")
    data.append({"client": client_name, "phone": client_phone, "goal": goal, "time": time})
    save("request.json", data)


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
    save("teachers.json", teachers)
    data = load("booking.json")
    data.append({"client": client_name, "phone": client_phone, "teacher": teacher_id, "day": day, "time": time})
    save("booking.json", data)
    return True


if __name__ == "__main__":
    save("teachers.json", teachers)
