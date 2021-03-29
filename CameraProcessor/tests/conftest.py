import pytest
import os


@pytest.fixture()
def get_images_dir():
    __root_dir = os.path.abspath(__file__ + '../../../../')
    __folder_name = 'test'
    __images_dir = f'{__root_dir}\\data\\annotated\\{__folder_name}\\img1'
    return __images_dir