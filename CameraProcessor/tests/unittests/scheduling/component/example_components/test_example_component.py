"""Import pytest and example_component.py for testing.

"""
import pytest
import processor.scheduling.component.example_components.example_component as example_component


def __eq__(self, other):
    """Custom equalize function

    Args:
        self: first object to compare
        other: second object to compare

    Returns: bool

    """
    if isinstance(self, other.__class__):
        return self.a == other.a and self.b == other.b
    return False


# pylint: disable=attribute-defined-outside-init
class TestExampleComponent():
    """Tests bounding_box.py.
    """

    # Setup
    def setup_method(self):
        """Setup method for testing.

        """
        self.first_arg = 'first arg'
        self.second_arg = 'second arg'
        self.work_expected_return = [self.first_arg, self.second_arg]

    def test_work(self):
        """Tests the functionality of work().

        """
        work_return = example_component.ExampleComponent.work(self.first_arg, self.second_arg)
        assert work_return.__eq__(self.work_expected_return)

    def test_execute_command(self):
        """Tests the functionality of execute_command().

        """
        work_return = example_component.ExampleComponent
        assert example_component.ExampleComponent.execute_component(work_return)

    def test_execute_command_invalid(self):
        """Tests the functionality of execute_command() with invalid value.

        """
        work_return = 'invalid input'
        with pytest.raises(Exception):
            assert example_component.ExampleComponent.execute_component(work_return)


if __name__ == '__main__':
    pytest.main(TestExampleComponent)
