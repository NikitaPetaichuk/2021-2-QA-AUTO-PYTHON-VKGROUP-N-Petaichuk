import allure
import pytest

from tests.api_tests.base_api import BaseCaseAPI


class TestUserManagement(BaseCaseAPI):

    def check_entity_existence(self, field, field_value, not_exists=True):
        user_entity = self.mysql_client.get_user(field, field_value)
        if not_exists:
            assert user_entity is None, "Unexpected user existence"
        else:
            assert user_entity is not None, "Unexpected user non-existence"

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User management API functionality')
    @allure.story('Checking correct API create user request')
    def test_correct_create_user(self):
        """
        Test for checking correct API create user request.
        Steps:
        1. Creating data for create user request.
        2. Making create user request.
        3. Checking user existence.
        Expected result:
        Response status code 201, user data is in DB.
        """
        with allure.step('Creating data for create user request'):
            user_data = self.user_builder.create_user_data()

        with allure.step('Making create user request'):
            self.check_request(self.api_client.post_add_user, user_data, 201)

        with allure.step('Checking user existence'):
            self.check_entity_existence("email", user_data["email"], not_exists=False)

        with allure.step('Tearing down: delete created user'):
            self.mysql_client.delete_user(user_data["email"])

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User management API functionality')
    @allure.story('Checking API create user request without one of required field')
    @pytest.mark.parametrize("field_to_delete", ["username", "email", "password"])
    def test_create_without_field(self, field_to_delete):
        """
        Test for checking API create user request without one of required field.
        Steps:
        1. Creating data for create user request.
        2. Making create user request.
        3. Checking user existence.
        Expected result:
        Response status code 400, user data is not in DB.
        """
        with allure.step('Creating data for create user request'):
            user_data = self.user_builder.create_user_data()
            del user_data[field_to_delete]

        with allure.step('Making create user request'):
            self.check_request(self.api_client.post_add_user, user_data, 400)

        with allure.step('Checking user existence'):
            user_email = user_data.get("email", None)
            self.check_entity_existence("email", user_email)

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User management API functionality')
    @allure.story('Checking API create user request with incorrect field value length')
    @pytest.mark.parametrize(
        "creation_settings",
        [
            {"username_size": 5},
            {"username_size": 17},
            {"email_prefix_size": 1},
            {"email_prefix_size": 61},
            {"password_size": 5},
            {"password_size": 256}
        ]
    )
    def test_create_with_incorrect_length(self, creation_settings):
        """
        Test for checking API create user request with incorrect field value length.
        Steps:
        1. Creating data for create user request.
        2. Making create user request.
        3. Checking user existence.
        Expected result:
        Response status code 400, user data is not in DB.
        """
        with allure.step('Creating data for create user request'):
            user_data = self.user_builder.create_user_data(**creation_settings)

        with allure.step('Making create user request'):
            self.check_request(self.api_client.post_add_user, user_data, 400)

        with allure.step('Checking user existence'):
            self.check_entity_existence("email", user_data["email"])

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User management API functionality')
    @allure.story('Checking API create user request with existent username/email value')
    @pytest.mark.parametrize("field_to_change", ["email", "username"])
    def test_create_user_with_same_field(self, field_to_change, faker):
        """
        Test for checking API create user request with existent username/email value.
        Steps:
        1. Creating user data.
        2. Adding user data to DB.
        3. Changing user data for create user request.
        4. Making create user request.
        5. Checking changed user existence.
        Expected result:
        Response status code 304, changed user data is not in DB.
        """
        with allure.step('Creating user data'):
            user_data = self.user_builder.create_user_data()

        with allure.step('Adding user data to DB'):
            self.mysql_client.add_user(user_data)

        with allure.step('Changing user data for create user request'):
            changed_user_data = user_data.copy()
            changed_user_data[field_to_change] = self.user_builder.create_user_data_string(16, 6)
            if field_to_change == "email":
                changed_user_data[field_to_change] += '@a.a'

        with allure.step('Making create user request'):
            self.check_request(self.api_client.post_add_user, changed_user_data, 304)

        with allure.step('Checking changed user existence'):
            self.check_entity_existence(field_to_change, changed_user_data[field_to_change])

        with allure.step('Tearing down: delete unchanged user from DB'):
            self.mysql_client.delete_user(user_data["email"])

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User management API functionality')
    @allure.story('Checking API create user request with invalid email value')
    def test_create_with_invalid_email(self):
        """
        Test for checking API create user request with invalid email value.
        Steps:
        1. Creating data for create user request.
        2. Making create user request.
        3. Checking user existence.
        Expected result:
        Response status code 400, user data is not in DB.
        """
        with allure.step('Creating data for create user request'):
            user_data = self.user_builder.create_user_data(correct_email=False)

        with allure.step('Making create user request'):
            self.check_request(self.api_client.post_add_user, user_data, 400)

        with allure.step('Checking user existence'):
            self.check_entity_existence("email", user_data["email"])

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User management API functionality')
    @allure.story('Checking API delete user request')
    def test_delete_user(self):
        """
        Test for checking API delete user request.
        Steps:
        1. Creating user data.
        2. Adding user data to DB.
        3. Making delete user request.
        4. Checking user existence.
        Expected result:
        Response status code 204, user data is not in DB.
        """
        with allure.step('Creating user data'):
            user_data = self.user_builder.create_user_data()

        with allure.step('Adding user data to DB'):
            self.mysql_client.add_user(user_data)

        with allure.step('Making delete user request'):
            self.check_request(self.api_client.get_user_delete, user_data["username"], 204)

        with allure.step('Checking user existence'):
            self.check_entity_existence("email", user_data["email"])

    @allure.epic('QA Python Final project: API testing')
    @allure.feature('User management API functionality')
    @allure.story('Checking API delete non-existent user request')
    def test_delete_non_existent_user(self, faker):
        """
        Test for checking API delete non-existent user request.
        Steps:
        1. Creating data for delete user request.
        2. Making delete user request.
        Expected result:
        Response status code 404.
        """
        with allure.step('Creating data for delete user request'):
            non_existent_username = self.user_builder.create_user_data_string(20, 0)

        with allure.step('Making delete user request'):
            self.check_request(self.api_client.get_user_delete, non_existent_username, 404)
