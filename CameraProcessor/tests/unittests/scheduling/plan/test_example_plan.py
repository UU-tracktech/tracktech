"""Import pytest and example_plan.py for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import runpy
import pytest
from tests.conftest import root_path


def test_example_plan():
    """Test example plan by running the file."""
    plan_path = os.path.join(root_path, 'processor', 'scheduling', 'plan', 'example_plan.py')
    runpy.run_path(plan_path)


if __name__ == '__main__':
    pytest.main(test_example_plan)
