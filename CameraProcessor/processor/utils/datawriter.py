"""Class with utils functions regarding the datawriter.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.data_writer.mot_data_writer import MotDataWriter
from processor.data_writer.json_data_writer import JsonDataWriter
from processor.data_writer.fake_data_writer import FakeDataWriter


def get_data_writer(configs, stage, file):
    """Method for getting the datawriter.

    Args:
        configs (ConfigParser): contianing the configs of the program.
        stage (string): either detection or tracking, for getting the correct format.
        file (string): file where the detections/tracks need to be written to.

    Returns:
         DataWriter: a datawriter that handles the data that needs to be written.
    """
    file_format = configs['Runner'][stage]
    if file_format.lower() == 'mot':
        return MotDataWriter(file)
    if file_format.lower() == 'json':
        return JsonDataWriter(file)
    return FakeDataWriter()
