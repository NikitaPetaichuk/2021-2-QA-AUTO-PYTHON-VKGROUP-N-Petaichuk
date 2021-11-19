import pytest

from business_logic.nginx_log_parser import MysqlNginxLogParser
from mysql_client.mysql_client import MysqlClient


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, nginx_log_parser, logger):
        self.mysql_client: MysqlClient = mysql_client
        self.nginx_log_parser: MysqlNginxLogParser = nginx_log_parser
        self.logger = logger

        self.logger.info("Initial setup complete")

    def get_table_entities(self, table_class):
        self.mysql_client.session.commit()
        return self.mysql_client.session.query(table_class).all()
