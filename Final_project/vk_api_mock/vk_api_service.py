import signal

from flask import Flask, jsonify, request
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)


USERS_DB = {}


@app.route('/vk_id/<username>', methods=['GET'])
def get_vk_id(username):
    if username in USERS_DB:
        vk_id_response = {"vk_id": USERS_DB[username]}
        return jsonify(vk_id_response), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Entity with the given username is not found"
        }), 404


@app.route('/vk_id/create_id', methods=['POST'])
def create_id():
    request_body = request.get_json()
    username = request_body.get("username", None)
    user_id = request_body.get("id", None)
    if username is not None and user_id is not None and username not in USERS_DB:
        USERS_DB[username] = user_id
        return jsonify({"status": "ok"}), 200
    else:
        if username in USERS_DB:
            return jsonify({
                "status": "error",
                "message": "Entity with the given username already exists"
            }), 400
        else:
            return jsonify({
                "status": "error",
                "message": "Incorrect JSON format (should be fields 'username' and 'id')"
            }), 400


@app.route('/vk_id/update_id', methods=['PUT'])
def update_id():
    request_body = request.get_json()
    username = request_body.get("username", None)
    new_id = request_body.get("new_id", None)
    if username is not None and new_id is not None and username in USERS_DB:
        USERS_DB[username] = new_id
        return jsonify({"status": "ok"}), 200
    else:
        if username not in USERS_DB:
            return jsonify({
                "status": "error",
                "message": "Entity with the given username is not found"
            }), 404
        else:
            return jsonify({
                "status": "error",
                "message": "Incorrect JSON format (should be fields 'username' and 'new_id')"
            }), 400


@app.route('/vk_id/delete_id/<username>', methods=['DELETE'])
def delete_id(username):
    if username in USERS_DB:
        del USERS_DB[username]
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Entity with the given username is not found"
        }), 404


class ServerTerminationError(Exception):
    pass


def exit_gracefully(signum, frame):
    raise ServerTerminationError()


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)


if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    try:
        app.run(host='0.0.0.0', port=9090)
    except ServerTerminationError:
        pass
