import pytest

from tests.api_tests.base_api import BaseCaseAPI


class TestUserManagement(BaseCaseAPI):

    def check_entity_existence(self, field, field_value, not_exists=True):
        user_entity = self.mysql_client.get_user(field, field_value)
        if not_exists:
            assert user_entity is None
        else:
            assert user_entity is not None

    def test_correct_create_user(self):
        user_data = self.user_builder.create_user_data()

        self.check_request(self.api_client.post_add_user, user_data, 201)

        self.check_entity_existence("email", user_data["email"], not_exists=False)

        self.mysql_client.delete_user(user_data["email"])

    @pytest.mark.parametrize("field_to_delete", ["username", "email", "password"])
    def test_create_without_field(self, field_to_delete):
        user_data = self.user_builder.create_user_data()
        del user_data[field_to_delete]

        self.check_request(self.api_client.post_add_user, user_data, 400)

        user_email = user_data.get("email", None)
        self.check_entity_existence("email", user_email)

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
        user_data = self.user_builder.create_user_data(**creation_settings)

        self.check_request(self.api_client.post_add_user, user_data, 400)

        self.check_entity_existence("email", user_data["email"])

    @pytest.mark.parametrize("field_to_change", ["email", "username"])
    def test_create_user_with_same_field(self, field_to_change, faker):
        user_data = self.user_builder.create_user_data()
        self.mysql_client.add_user(user_data)
        user_data[field_to_change] = faker.unique.pystr(max_chars=16)
        if field_to_change == "email":
            user_data[field_to_change] += '@a.a'

        self.check_request(self.api_client.post_add_user, user_data, 304)

        self.check_entity_existence(field_to_change, user_data[field_to_change])

    def test_create_with_invalid_email(self):
        user_data = self.user_builder.create_user_data(correct_email=False)

        self.check_request(self.api_client.post_add_user, user_data, 400)

        self.check_entity_existence("email", user_data["email"])

    def test_delete_user(self):
        user_data = self.user_builder.create_user_data()
        self.mysql_client.add_user(user_data)

        self.check_request(self.api_client.get_user_delete, user_data["username"], 204)

        self.check_entity_existence("email", user_data["email"])

    def test_delete_non_existent_user(self, faker):
        non_existent_username = faker.pystr(max_chars=20, min_chars=0)

        self.check_request(self.api_client.get_user_delete, non_existent_username, 404)
