import logging
import threading

from flask import Flask
from werkzeug.serving import make_server


class FlaskThreadExecutor:

    def __init__(self, app, host, port, log_path):
        self.app: Flask = app
        self.host = host
        self.port = port
        self.server = None
        self.server_thread = None
        self.log_path = log_path
        self._create_logger(log_path)

    @staticmethod
    def _create_logger(log_path):
        log_formatter = logging.Formatter("%(asctime)s - werkzeug - %(levelname)s - '%(message)s'")
        log_level = logging.DEBUG

        file_handler = logging.FileHandler(log_path, 'w')
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(log_level)

        logging.getLogger("werkzeug").addHandler(file_handler)

    def start(self):
        self.server = make_server(self.host, self.port, self.app)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server_thread.join()
