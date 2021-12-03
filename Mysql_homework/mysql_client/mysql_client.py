import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from models.model import Base


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

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        mysql_url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}?charset=utf8mb4'

        self.engine = sqlalchemy.create_engine(mysql_url)
        self.connection = self.engine.connect()

        session_maker = sessionmaker(bind=self.connection.engine)
        self.session = session_maker()

    def execute_query(self, query, fetch_result=False):
        sql_query = sqlalchemy.text(query)
        result = self.connection.execute(sql_query)
        if fetch_result:
            return result.fetchall()

    def recreate_test_db(self):
        self.connect(db_created=False)

        self.execute_query(f"DROP database if exists {self.db_name}")
        self.execute_query(f"CREATE database {self.db_name}")

        self.connection.close()
        self.connect()

    def create_table(self, table_name):
        if not inspect(self.engine).has_table(table_name):
            Base.metadata.tables[table_name].create(self.engine)

    def create_test_tables(self, test_tables_list):
        for table_name in test_tables_list:
            self.create_table(table_name)
