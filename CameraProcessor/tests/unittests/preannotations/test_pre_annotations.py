import os
import pytest
from src.training.pre_annotations import PreAnnotations

example_text_file = os.path.join(__file__, '../example_pre_annotations.txt')
example_json_file = os.path.join(__file__, '../example_pre_annotations.json')


@pytest.mark.parametrize('nr_frames', [-2, -1, 0, 1, 5])
def test_constructor(nr_frames):
    if nr_frames < 0:
        assert pytest.raises(AttributeError, PreAnnotations, example_text_file, nr_frames)
        return
    annotations = PreAnnotations(example_text_file, nr_frames)
    assert annotations.nr_frames == nr_frames
    assert annotations.file_path == example_text_file
    assert len(annotations.boxes) == nr_frames
