from flask import jsonify


class ResponseBuilder:

    @staticmethod
    def create_ok_response(response_data=None):
        response_body = {
            "status": "ok"
        }
        if response_data is not None:
            for key, value in response_data.items():
                response_body[key] = value
        return jsonify(response_body), 200

    @staticmethod
    def create_not_json_response():
        response_body = {
            "status": "error",
            "message": "Expected JSON data, got non-JSON data"
        }
        return jsonify(response_body), 400

    @staticmethod
    def create_no_json_field_response(json_field):
        response_body = {
            "status": "error",
            "message": f"Incorrect JSON format: field '{json_field}' doesn't found"
        }
        return jsonify(response_body), 400

    @staticmethod
    def create_no_user_response(user_id):
        response_body = {
            "status": "error",
            "message": f"User with identifier '{user_id}' doesn't exist"
        }
        return jsonify(response_body), 404
