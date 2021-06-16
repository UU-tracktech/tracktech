"""File that contains method to create authorisation parameters.

This file sets up the tornado application.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import os

from auth.auth import Auth
import src.utility.logger as logger


def get_auth_params():
    """Uses environment variables to create authentication parameters for the tornado application.

    Returns:
        Auth, Auth: Objects for the client and processor if keys were provided in the environment variables.
    """
    public_key, audience = os.environ.get('PUBLIC_KEY'), os.environ.get('AUDIENCE')
    client_auth, processor_auth = None, None
    # Only activate authentication if required environment variables are set.
    if public_key is not None and audience is not None:
        client_role = os.environ.get('CLIENT_ROLE')
        # Client and Processor authentication can be used independently.
        if client_role is not None:
            logger.log('using client token validation.')
            client_auth = Auth(public_key_path=public_key, algorithms=['RS256'],
                               audience=audience, role=client_role)
        processor_role = os.environ.get('PROCESSOR_ROLE')
        if processor_role is not None:
            logger.log('using processor token validation.')
            processor_auth = Auth(public_key_path=public_key, algorithms=['RS256'],
                                  audience=audience, role=processor_role)

    return client_auth, processor_auth
