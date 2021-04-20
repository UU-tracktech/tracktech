"""Import pytest and example_plan.py for testing.

"""
import os
import runpy
import pytest
from tests.conftest import root_path


def test_example_plan():
    """Test example plan by running the file

    """
    plan_path = os.path.join(root_path, 'processor', 'scheduling', 'plan', 'example_plan.py')
    runpy.run_path(plan_path)


if __name__ == '__main__':
    pytest.main(test_example_plan)
