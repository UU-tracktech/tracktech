"""Tests update_message.py.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from processor.webhosting.update_command import UpdateCommand


# pylint: disable=attribute-defined-outside-init
class TestUpdateCommand:
    """Tests the update command."""

    def setup_method(self):
        """Creates a UpdateMessage object."""
        self.update = UpdateCommand([0.1] * 512, 1)

    def test_update_command(self):
        """Asserts if UpdateMessage object has been initialized correctly."""
        assert self.update.feature_map == [0.1] * 512
        assert self.update.object_id == 1


if __name__ == '__main__':
    pytest.main(TestUpdateCommand)
