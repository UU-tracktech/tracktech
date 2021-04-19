"""Import pytest and output_component.py for testing.

"""
import pytest
import processor.scheduling.component.example_components.output_component as output_component


# pylint: disable=attribute-defined-outside-init
class TestOutputComponent():
    """Tests bounding_box.py.
    """

    # Setup
    def setup_method(self):
        """Setup method for testing.

        """
        self.first_arg = 'first arg'
        self.work_expected_return = self.first_arg

    def test_execute_command(self):
        """Tests the functionality of execute_command().

        """
        work_return = output_component.OutputComponent
        assert output_component.OutputComponent.execute_component(work_return)

    def test_execute_command_invalid(self):
        """Tests the functionality of execute_command__invalid().

        """
        work_return = 'invalid input'
        with pytest.raises(Exception):
            assert output_component.OutputComponent.execute_component(work_return)

    def test_execute_command_intermedairy(self):
        """Tests the functionality of execute_command() in IntermedairyOutputComponent.

        """
        work_return = output_component.IntermediaryOutputComponent
        assert output_component.IntermediaryOutputComponent.execute_component(work_return)

    def test_execute_command_invalid_intermedairy(self):
        """Tests the functionality of execute_command() in IntermedairyOutputComponent with invalid value.

        """
        work_return = 'invalid input'
        with pytest.raises(Exception):
            assert output_component.IntermediaryOutputComponent.execute_component(work_return)


if __name__ == '__main__':
    pytest.main(TestOutputComponent)
