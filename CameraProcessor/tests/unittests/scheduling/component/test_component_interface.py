"""Import pytest and component_interface.py for testing.

"""
import pytest
import processor.scheduling.component.component_interface as component_interface


# pylint: disable=attribute-defined-outside-init
class TestComponentInterface:
    """Tests bounding_box.py.
    """

    # Setup
    def setup_method(self):
        """Setup method for testing.

        """
        self.first_arg = 'first arg'

    def test_execute_command(self):
        """Tests the functionality of execute_command().

        """
        with pytest.raises(NotImplementedError):
            assert component_interface.IComponent.execute_component(self.first_arg)


if __name__ == '__main__':
    pytest.main(TestComponentInterface)
