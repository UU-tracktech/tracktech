"""Import pytest and base_component.py for testing.

"""
import pytest
import processor.scheduling.component.base_component as base_component


# pylint: disable=attribute-defined-outside-init
class TestBaseComponent:
    """Tests bounding_box.py.
    """

    # Setup
    def setup_method(self):
        """Setup method for testing.

        """
        self.first_arg = 'first arg'

    def test_execute_component(self):
        """Tests the functionality of BaseComponent(execute_component())

        """
        with pytest.raises(Exception):
            assert base_component.BaseComponent.execute_component(self.first_arg)


if __name__ == '__main__':
    pytest.main(TestBaseComponent)
