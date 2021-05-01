"""Tests pre annotations for each file type to see whether data is loaded in correctly

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import pytest
from processor.training.pre_annotations import PreAnnotations
from tests.conftest import root_path


example_text_file = os.path.join(root_path, 'data/tests/unittests/example_pre_annotations.txt')
example_json_file = os.path.join(root_path, 'data/tests/unittests/example_pre_annotations.json')
example_py_file = os.path.join(os.path.dirname(__file__), 'example_pre_annotations.py')


@pytest.mark.parametrize('nr_frames', [0, 1, 5])
def test_constructor(nr_frames: int) -> None:
    """Tests constructor with valid number of frames

    Args:
        nr_frames (int): Positive number of frames

    """
    # Test the annotations object
    annotations = PreAnnotations(example_text_file, nr_frames)
    assert annotations.nr_frames == nr_frames
    assert annotations.file_path == example_text_file
    assert len(annotations.boxes) == nr_frames


@pytest.mark.parametrize('neg_nr_frames', [-5, -2, -1])
def test_constructor_invalid(neg_nr_frames: int) -> None:
    """Tests whether constructor raises exception when called with negative number of frames

    Args:
        neg_nr_frames (int): Negative number of frames the annotations are made with

    """
    assert pytest.raises(AttributeError, PreAnnotations, example_text_file, neg_nr_frames)


def test_invalid_file_format() -> None:
    """Tests whether an invalid format is caught when trying to parse the file
    """
    pre_annotations = PreAnnotations(example_py_file, 1)
    assert pytest.raises(NotImplementedError, pre_annotations.parse_file)
