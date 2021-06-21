"""Class with utils functions regarding the datawriter.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.data_writer.mot_data_writer import MotDataWriter
from processor.data_writer.json_data_writer import JsonDataWriter
from processor.data_writer.fake_data_writer import FakeDataWriter


def get_data_writer(configs, stage, file):
    """'detection' of 'tracking'"""
    file_format = configs['Runner'][stage]
    if file_format.lower() == 'mot':
        return MotDataWriter(file)
    if file_format.lower() == 'json':
        return JsonDataWriter(file)
    else:
        return FakeDataWriter()