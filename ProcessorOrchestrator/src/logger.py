"""Logging component that contains a few util methods for logging.

The functions defined can be used from other points in the program to easily create
log entries formatted in a standardised manner.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import logging

logging.basicConfig(filename='logs.log',
                    format='%(asctime)s | %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def log(message):
    """Writes a general message to the log

    Args:
        message:
            The message to be logged.
    """
    logging.info(message)
    print(message)


def log_get_request(location, ip_address):
    """Writes a get request to the log.

    Args:
        location:
            Url path where this request was made.
        ip_address:
            Ip address of the request origin.
    """
    message = f"GET Request made for {location} from {ip_address}"
    logging.info(message)
    print(message)


def log_message_receive(message, location, ip_address):
    """Logs a message that was received.

    Args:
        message:
            The message that was received.
        location:
            Url path where this request was made.
        ip_address:
            Ip address where the message was sent from.
    """
    message = f"Received message on {location} from {ip_address}: {message}"
    logging.info(message)
    print(message)


def log_message_send(message, location, ip_address):
    """Logs a message that was sent.

        Args:
            message:
                The message that was sent.
            location:
                Url path where this request was made.
            ip_address:
                Ip address where the message was sent to.
    """
    message = f"Sent message on {location} from {ip_address}: {message}"
    logging.info(message)
    print(message)


def log_connect(location, ip_address):
    """Logs a new websocket connection.

        Args:
            location:
                Url path where this connection was made.
            ip_address:
                Ip address of the connection origin.
    """
    message = f"Websocket connected on {location} from {ip_address}"
    logging.info(message)
    print(message)


def log_disconnect(location, ip_address):
    """Logs a new websocket connection.

        Args:
            location:
                Url path where this connection was stopped.
            ip_address:
                Ip address of the connection origin.
    """
    message = f"Websocket disconnected on {location} from {ip_address}"
    logging.info(message)
    print(message)


def log_error(location, error, ip_address):
    """Logs an error.

        Args:
            location:
                Url path where this error was handled.
            error:
                The error that was handled.
            ip_address:
                Ip address of the source of the error.
    """
    message = f"{error} on {location} from {ip_address}"
    logging.warning(message)
    print(message)
