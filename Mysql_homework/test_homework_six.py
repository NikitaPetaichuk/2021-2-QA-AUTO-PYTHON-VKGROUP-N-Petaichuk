import allure
import pytest

from base import BaseCase
from models.model import RequestsCount, MethodsCount, PopularRequests, Biggest4XXRequests, Popular5XXRequestsIP


class TestHomeworkSix(BaseCase):

    def check_rows_count(self, table_class, expected_rows_count):
        entities = self.get_table_entities(table_class)
        assert len(entities) == expected_rows_count

    @allure.epic('QA Python Homework 6: MySQL testing')
    @allure.feature('Working with access log data')
    @allure.story('Check inserting to requests count table')
    @pytest.mark.Mysql
    def test_requests_count(self):
        with allure.step('Sending requests count data to DB'):
            sent_rows_count = self.nginx_log_parser.write_to_db_requests_count()

        with allure.step(f'Checking {RequestsCount.__name__} table rows count'):
            self.check_rows_count(RequestsCount, sent_rows_count)

    @allure.epic('QA Python Homework 6: MySQL testing')
    @allure.feature('Working with access log data')
    @allure.story('Check inserting to methods count table')
    @pytest.mark.Mysql
    def test_methods_count(self):
        with allure.step('Sending methods count data to DB'):
            sent_rows_count = self.nginx_log_parser.write_to_db_methods_count()

        with allure.step(f'Checking {MethodsCount.__name__} table rows count'):
            self.check_rows_count(MethodsCount, sent_rows_count)

    @allure.epic('QA Python Homework 6: MySQL testing')
    @allure.feature('Working with access log data')
    @allure.story('Check inserting to popular requests table')
    @pytest.mark.Mysql
    def test_popular_requests(self):
        with allure.step('Sending requests count data to DB'):
            sent_rows_count = self.nginx_log_parser.write_to_db_10_popular_requests()

        with allure.step(f'Checking {PopularRequests.__name__} table rows count'):
            self.check_rows_count(PopularRequests, sent_rows_count)

    @allure.epic('QA Python Homework 6: MySQL testing')
    @allure.feature('Working with access log data')
    @allure.story('Check inserting to biggest requests (with 4XX status code) table')
    @pytest.mark.Mysql
    def test_biggest_4xx_requests(self):
        with allure.step('Sending requests count data to DB'):
            sent_rows_count = self.nginx_log_parser.write_to_db_5_biggest_4xx_requests()

        with allure.step(f'Checking {Biggest4XXRequests.__name__} table rows count'):
            self.check_rows_count(Biggest4XXRequests, sent_rows_count)

    @allure.epic('QA Python Homework 6: MySQL testing')
    @allure.feature('Working with access log data')
    @allure.story('Check inserting to popular requests ip (with 5XX status code) table')
    @pytest.mark.Mysql
    def test_popular_5xx_requests_ip(self):
        with allure.step('Sending requests count data to DB'):
            sent_rows_count = self.nginx_log_parser.write_to_db_5_popular_5xx_requests_ip()

        with allure.step(f'Checking {Popular5XXRequestsIP.__name__} table rows count'):
            self.check_rows_count(Popular5XXRequestsIP, sent_rows_count)
