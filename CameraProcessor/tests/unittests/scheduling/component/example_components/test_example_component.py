import pytest
import processor.scheduling.component.example_components.example_component


# pylint: disable=attribute-defined-outside-init
class ExampleComponent:
    """Tests bounding_box.py.
    """

    # Setup
    def setup_method(self):
        pass


if __name__ == '__main__':
    pytest.main(ExampleComponent)
