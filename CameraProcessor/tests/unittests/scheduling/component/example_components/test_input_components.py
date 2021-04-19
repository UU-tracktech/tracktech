"""Import pytest and input_componenet.py for testing.

"""
import pytest
import processor.scheduling.component.example_components.input_component as input_component


# pylint: disable=attribute-defined-outside-init
class TestInputComponent():
    """Tests bounding_box.py.
    """

    # Setup
    def setup_method(self):
        """Setup method for testing.

        """
        self.first_arg = 'first arg'
        self.work_expected_return = self.first_arg

    def test_work(self):
        """Tests the functionality of work().

        """
        work_return = input_component.InputComponent.work(self.first_arg)
        assert work_return.__eq__(self.work_expected_return)

    def test_execute_command(self):
        """Tests the functionality of execute_command().

        """
        work_return = input_component.InputComponent
        assert input_component.InputComponent.execute_component(work_return)

    def test_execute_command_invalid(self):
        """Tests the functionality of execute_command() with invalid value.

        """
        work_return = 'invalid input'
        with pytest.raises(Exception):
            assert input_component.InputComponent.execute_component(work_return)


if __name__ == '__main__':
    pytest.main(TestInputComponent)
