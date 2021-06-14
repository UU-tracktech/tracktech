"""Gets the token given an authentication server url. Uses the client_secret OAuth2 flow.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import logging
import requests


def get_token(auth_server_url):
    """Retrieves the client_id and client_secret from the environment and requests token from authentication url.

    Args:
        auth_server_url (str): Url of the authentication server to request the token from.

    Returns:
        str: Access token received from the authentication server.

    Raises:
        AttributeError: Authentication credentials given in the environment are invalid.
        EnvironmentError: Whenever the environment variables were not found in the environment.
        ConnectionError: No response from the authentication server.
    """
    # Get environment variables.
    client_id = os.environ.get('CLIENT_ID', None)
    client_secret = os.environ.get('CLIENT_SECRET', None)

    # Environment variables not found.
    if client_id is None or client_secret is None:
        logging.error('Retrieving token without environment variables')
        raise EnvironmentError('CLIENT_ID or CLIENT_SECRET not found in environment.')

    params = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    # Post request given the parameters.
    response = requests.post(auth_server_url, params)

    if response.status_code == 401:
        raise AttributeError('Authentication credentials are invalid.')

    # Authentication server gave back an error response.
    if response.status_code != 200:
        raise ConnectionError('Could not request the token from the authentication server.')

    # Return the token.
    content = response.json()
    return content['access_token']
