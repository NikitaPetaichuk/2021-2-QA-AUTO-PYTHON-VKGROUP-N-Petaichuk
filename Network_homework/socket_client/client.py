import json
import logging
import socket
from urllib.parse import urlencode

from static.tests_config import TestsConfig


class SocketClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.logger = logging.getLogger(TestsConfig.TESTS_LOGS_NAME)

    def _create_connection(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.settimeout(10)
        connection.connect((self.host, self.port))
        return connection

    def _create_request(self, method, path, headers, body):
        request = f"{method} {path} HTTP/1.1\r\nHost: {self.host}\r\nConnection: close\r\n"
        if headers is not None:
            for header, value in headers.items():
                request += f"{header}: {value}\r\n"
        if body is not None:
            if headers['Content-Type'].startswith("application/json"):
                body = json.dumps(body)
            elif headers['Content-Type'].startswith("application/x-www-form-urlencoded"):
                body = urlencode(body)
            request += f"Content-Length: {len(body)}\r\n"
        request += "\r\n"
        if body is not None:
            request += f"{body}\r\n"
        return request

    def _read_response(self, connection):
        received_data = []
        while True:
            data = connection.recv(4096)
            if data:
                received_data.append(data.decode())
            else:
                break
        return self._parse_response(received_data)

    @staticmethod
    def _parse_response(raw_response):
        raw_response = ''.join(raw_response).splitlines()
        status_code = int(raw_response[0].split()[1])
        headers = {}
        for header_string in raw_response[1:]:
            if header_string == '':
                break
            header, value = header_string.split(": ", maxsplit=1)
            headers[header] = value
        body = json.loads(raw_response[-1])
        return {
            "status_code": status_code,
            "headers": headers,
            "body": body
        }

    def _log_response(self, response):
        start_part = "Got response from server:"
        status_code_part = f"STATUS CODE: {response['status_code']}"
        headers_content = '\n'.join([f"{k}: {v}" for k, v in response["headers"].items()])
        headers_part = f"HEADERS:\n{headers_content}"
        body_part = f"BODY:\n{json.dumps(response['body'])}"
        self.logger.info(f"{start_part}\n{status_code_part}\n{headers_part}\n{body_part}\n\n")

    def make_request(self, method, path, headers=None, body=None):
        connection = self._create_connection()
        request = self._create_request(method, path, headers, body)
        connection.send(request.encode())
        response = self._read_response(connection)
        connection.close()
        self._log_response(response)
        return response

