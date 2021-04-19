"""Import pytest and example_plan.py for testing.

"""
import pytest


# pylint: disable=attribute-defined-outside-init
class TestPlan():
    """Tests bounding_box.py.
    """

    # Setup
    def setup_method(self):
        """Setup method for testing.

        """

    def test_example_plan(self):
        """Automatic pass due to lack of functions in example_plan.py

        """


if __name__ == '__main__':
    pytest.main(TestPlan)
