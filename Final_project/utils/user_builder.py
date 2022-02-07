import time

from faker import Faker


class UserBuilder:

    def __init__(self):
        self.fake = Faker()
        Faker.seed(int(time.time_ns()))

    def create_user_data(self, username_size=None, email_prefix_size=None, password_size=None, correct_email=True):
        username_size = 16 if username_size is None else username_size
        email_prefix_size = 40 if email_prefix_size is None else email_prefix_size
        password_size = 10 if password_size is None else password_size

        username = self.fake.unique.pystr(max_chars=username_size) if username_size > 0 else None
        if email_prefix_size > 0:
            email = self.fake.unique.pystr(max_chars=email_prefix_size) + ('@a.a' if correct_email else '')
        else:
            email = None
        password = self.fake.unique.pystr(max_chars=password_size) if password_size > 0 else None
        return {
            "username": username,
            "email": email,
            "password": password
        }

    def create_user_data_string(self, max_chars, min_chars=None):
        return self.fake.unique.pystr(max_chars=max_chars, min_chars=min_chars)
