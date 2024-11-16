from aiogram.fsm.state import StatesGroup, State
import re


class SignupStates(StatesGroup):
    name = State()
    age = State()
    phone = State()
    job = State()
    goal = State()
    verify = State()


phone_regex = re.compile(r"(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+")


def check_phone(user_input):
    if re.fullmatch(phone_regex, user_input):
        user_input = "phone"

    else:
        user_input = "error"

    return user_input


users = {
    '1236641': {'refer_id': '1726123039', 'flag': True, 'user_name': 'Jon'},
    '1236642': {'refer_id': '1726123039', 'flag': True, 'user_name': 'Bobur'},
    '1726123039': {'refer_id': None, 'flag': True, 'user_name': 'Jon'},
    '1236643': {'refer_id': '1726123039', 'flag': True, 'user_name': 'Jamshit'},
}


class GetUserName(StatesGroup):
    name = State()


def get_user_ball(user_id):  # 1726123039
    ball = 0
    l = []
    for user in users.values():
        if user_id == user['refer_id'] and user['flag'] == True:
            ball += 1
            l.append(user['user_name'])
    return f"{ball} Ball\n\nUserlar:\n{l}"
