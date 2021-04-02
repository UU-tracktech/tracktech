"""Logging component that contains a few util methods for logging.

The functions defined can be used from other points in the program to easily create
log entries formatted in a standardised manner.
"""

import logging

logging.basicConfig(filename='logs.log',
                    format='%(asctime)s | %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def log_get_request(location, ip):
    """Writes a get request to the log.

    Args:
        location:
            Url path where this request was made.
        ip:
            Ip address of the request origin.
    """
    logging.info(f"GET Request made for {location} from {ip}")


def log_message_receive(message, location, ip):
    """Logs a message that was received.

    Args:
        message:
            The message that was received.
        location:
            Url path where this request was made.
        ip:
            Ip address where the message was sent from.
    """
    logging.info(f"Received message on {location} from {ip}: {message}")


def log_message_send(message, location, ip):
    """Logs a message that was sent.

        Args:
            message:
                The message that was sent.
            location:
                Url path where this request was made.
            ip:
                Ip address where the message was sent to.
    """
    logging.info(f"Sent message on {location} from {ip}: {message}")


def log_connect(location, ip):
    """Logs a new websocket connection.

        Args:
            location:
                Url path where this connection was made.
            ip:
                Ip address of the connection origin.
    """
    logging.info(f"Websocket connected on {location} from {ip}")


def log_disconnect(location, ip):
    """Logs a new websocket connection.

        Args:
            location:
                Url path where this connection was stopped.
            ip:
                Ip address of the connection origin.
    """
    logging.info(f"Websocket disconnected on {location} from {ip}")


def log_error(location, error, ip):
    """Logs an error.

        Args:
            location:
                Url path where this error was handled.
            error:
                The error that was handled.
            ip:
                Ip address of the source of the error.
    """
    logging.warning(f"{error} on {location} from {ip}")
