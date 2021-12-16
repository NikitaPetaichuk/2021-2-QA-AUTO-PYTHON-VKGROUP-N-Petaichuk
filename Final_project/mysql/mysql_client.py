import logging

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from mysql.models.model import TestUsers


class MysqlClient:

    def __init__(self, user, password, db_name, host='127.0.0.1', port=3306):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.host = host
        self.port = port
        self.engine = None
        self.connection = None
        self.session = None
        self.logger = logging.getLogger('tests')

    def connect(self):
        mysql_url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/' \
                    f'{self.db_name}?charset=utf8mb4'
        self.engine = sqlalchemy.create_engine(mysql_url)
        self.connection = self.engine.connect()

        session_maker = sessionmaker(bind=self.connection.engine)
        self.session = session_maker()

    def add_user(self, user_data):
        self.logger.info(f"Adding user data '{user_data}' to DB")

        user_entity = TestUsers(**user_data, access=1)
        self.session.add(user_entity)
        self.session.commit()

    def delete_user(self, user_email):
        self.logger.info(f"Deleting user with email '{user_email}' from DB")

        self.session.commit()
        self.session.query(TestUsers).filter(TestUsers.email == user_email).delete()
        self.session.commit()

    def get_user(self, field, value):
        self.logger.info(f"Getting user with {field} == '{value}'")

        self.session.commit()
        return self.session.query(TestUsers).filter(getattr(TestUsers, field) == value).first()

    def set_user_access(self, user_email, access_status):
        self.logger.info(f"Setting access to '{access_status}' for user with email '{user_email}'")

        self.session.commit()
        self.session.query(TestUsers).filter(TestUsers.email == user_email).update({"access": access_status})
        self.session.commit()
