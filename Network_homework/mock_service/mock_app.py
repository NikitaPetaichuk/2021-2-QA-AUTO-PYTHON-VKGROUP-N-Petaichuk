from flask import Flask, request
from flask.views import MethodView

from utils.builders.response_builder import ResponseBuilder

app = Flask(__name__)


users_storage = {}
next_user_id = 1


class UserMockAPI(MethodView):

    def post(self):
        global next_user_id

        body = request.get_json()
        if body is None:
            return ResponseBuilder.create_not_json_response()
        elif "name" not in body:
            return ResponseBuilder.create_no_json_field_response("name")
        elif "surname" not in body:
            return ResponseBuilder.create_no_json_field_response("surname")

        users_storage[next_user_id] = {
            "name": body["name"],
            "surname": body["surname"]
        }
        response = ResponseBuilder.create_ok_response({"id": next_user_id})
        next_user_id += 1
        return response

    def get(self, user_id):
        if users_storage.get(user_id, None) is None:
            return ResponseBuilder.create_no_user_response(user_id)
        return ResponseBuilder.create_ok_response({"user": users_storage[user_id]})

    def put(self, user_id):
        if users_storage.get(user_id, None) is None:
            return ResponseBuilder.create_no_user_response(user_id)

        body = request.get_json()
        if body is None:
            return ResponseBuilder.create_not_json_response()

        if "name" in body:
            users_storage[user_id]["name"] = body["name"]
        if "surname" in body:
            users_storage[user_id]["surname"] = body["surname"]
        return ResponseBuilder.create_ok_response()

    def delete(self, user_id):
        if users_storage.get(user_id, None) is None:
            return ResponseBuilder.create_no_user_response(user_id)

        users_storage.pop(user_id, None)
        return ResponseBuilder.create_ok_response()


user_view = UserMockAPI.as_view('user_api')
app.add_url_rule('/users/', view_func=user_view, methods=['POST'])
app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])
