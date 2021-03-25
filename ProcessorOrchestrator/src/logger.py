from datetime import datetime
from tornado.web import RequestHandler
import logging

logging.basicConfig(filename='logs.log', format='%(asctime)s | %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


class LogHandler(RequestHandler):
    def get(self):
        f = open("logs.log", "r")
        self.write(f.read().replace("\n", "<br/>"))


def log_get_request(location, ip):
    logging.info(f"GET Request made for {location} from {ip}")


def log_message_receive(message, location, ip):
    logging.info(f"Received message on {location} from {ip}: {message}")


def log_message_send(message, location, ip):
    logging.info(f"Sent message on {location} from {ip}: {message}")


def log_connect(location, ip):
    logging.info(f"Websocket connected on {location} from {ip}")


def log_disconnect(location, ip):
    logging.info(f"Websocket disconnected on {location} from {ip}")


def log_error(location, error, ip):
    logging.warning(f"{error} on {location} from {ip}")