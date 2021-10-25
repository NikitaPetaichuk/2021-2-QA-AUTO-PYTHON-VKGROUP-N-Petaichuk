import random
import string
import time


def generate_spaces_string():
    random.seed()
    return ' ' * random.randint(1, 10)


def generate_invalid_password():
    random.seed()
    password_size = random.randint(6, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=password_size))


def generate_name(prefix):
    random.seed()
    random_part_size = random.randint(4, 6)
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=random_part_size))
    return f"{prefix}_{random_part}_{time.time()}"
