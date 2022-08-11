import random
import string


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_username() -> str:
    return f"test_user{random_lower_string()}"

def random_room_name() -> str:
    return f"test_room{random_lower_string()}"

def random_room_type() -> str:
    return random.choice(["group", "dm", "timecapsule"])