import os
import requests
import logging


def get_token(url):
    """Retrieves the client_id and client_secret from the environment and requests token from url.

    Args:
        url (str): Url of the authentication server.

    Returns:
        str: Access token recieved from the authentication server

    Raises:
        EnvironmentError: Whenever the environment variables were not found in the environment.
        ConnectionError: No response from the authentication server.
    """
    # Get environment variables.
    client_id = os.environ.get('client_id', None)
    client_secret = os.environ.get('client_secret', None)

    # Environment variables not found.
    if client_id is None or client_secret is None:
        logging.error(f'Retrieving token without environment variables')
        raise EnvironmentError('client_id or client_secret not found in environment.')

    params = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    # Post request given the parameters.
    response = requests.post(url, params)

    # Authentication server gave back an error response.
    if response.status_code != 200:
        raise ConnectionError('Could not request the token from the authentication server.')

    # Return the token.
    content = response.json()
    return content['access_token']
