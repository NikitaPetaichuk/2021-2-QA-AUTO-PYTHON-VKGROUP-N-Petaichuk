import time

from faker import Faker


class UserBuilder:

    def __init__(self):
        self.fake = Faker()
        Faker.seed(int(time.time()))

    def create_user_entity(self, user_id_min, user_id_max, name=None, surname=None):
        user_id = self.fake.unique.pyint(user_id_min, user_id_max)
        return {
            "id": user_id,
            "data": self.create_user_data(name, surname)
        }

    def create_user_data(self, name=None, surname=None):
        if name is None:
            name = self.fake.first_name()
        if surname is None:
            surname = self.fake.last_name()
        return {
            "name": name,
            "surname": surname
        }
