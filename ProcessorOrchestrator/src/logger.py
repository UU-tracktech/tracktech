from datetime import datetime
from tornado.web import RequestHandler


class LogHandler(RequestHandler):
    def get(self):
        f = open("logs.txt", "r")
        self.write(f.read())


def write_to_log(text):
    f = open("logs.txt", "a")
    f.write(f"\n{datetime.now()} | {text}")
    f.close()


def log_message_receive(message, location, ip):
    write_to_log(f"Received message on {location} from {ip}: {message}")


def log_message_send(message, location, ip):
    write_to_log(f"Sent message on {location} from {ip}: {message}")


def log_connect(location, ip):
    write_to_log(f"Websocket connected on {location} from {ip}")


def log_disconnect(location, ip):
    write_to_log(f"Websocket disconnected on {location} from {ip}")


def log_error(location, error, ip):
    write_to_log(f"{error} on {location} from {ip}")