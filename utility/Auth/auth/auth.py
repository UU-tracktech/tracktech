"""Handles authentication and authorization of tokens.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import jwt

from AuthenticationError import AuthenticationError
from AuthorizationError import AuthorizationError

class Auth:
    """Keeps track of authentication options in order to validate tokens. """
    def __init__(self, public_key_path, algorithms, audience, role):
        """Constructor.

        Args:
            public_key_path (str): the path to the public key file
            algorithms (list): the algorithms to use to validate the token
            audience (iterable): the audience for the token
            role (str): the role the user needs
        """

        # Read the key file.
        public_key_file = open(public_key_path, "r")
        self.public_key = public_key_file.read()
        public_key_file.close()

        # Save the other arguments.
        self.algorithms = algorithms
        self.audience = audience
        self.role = role

    def validate(self, token) -> None:
        """Validate the given token.

        Args:
            token (str): an jwt token to validate
        """

        try:
            # Decode the token using the given key and the header token.
            decoded = jwt.decode(token, self.public_key, algorithms=self.algorithms, audience=self.audience)

        except Exception as e:
            # If decoding fails throw a AuthenticationError.
            raise AuthenticationError("Failed to authorize", e) from e

        try:
            authorized = self.role in decoded["resource_access"][self.audience]["roles"]
            # If decoding succeeds but the role is invalid throw a AuthorizationError.

        except Exception as e:
            # If decoding fails throw a AuthenticationError.
            raise AuthenticationError("Failed to authorize", e) from e

        if not authorized:
            raise AuthorizationError("Role not found")

        print("Authed")

