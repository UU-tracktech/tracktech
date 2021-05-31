"""Loads json data from json file containing messages that can be sent to the orchestrator.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import json
import random
from tests.conftest import root_path


def load_data(datatype, number=1, rng=False):
    """Load a JSON test data file of chosen type.

    Args:
        datatype (str): One of these options ['boundingBoxes', 'start', 'stop', 'featureMap', 'invalid'].
        number (int): A number which will load 'nr' random json objects if not None.
        rng (bool): Whether or not to load data in a random order.

    Returns:
        dict[str, str]: A dictionary of test data of the chosen JSON message type.
    """
    switcher = {
        'boundingBoxes': 'boxes',
        'start': 'start',
        'stop': 'stop',
        'featureMap': 'featuremaps',
        'invalid': 'invalid',
        'bad': 'baddata',
        'full': 'startfeaturestop'
    }

    # Gets file name.
    filename = switcher.get(datatype)
    if not filename:
        raise NameError('The JSON object requested is not in scope.')

    # File path and load content.
    json_name = filename + '.json'
    json_path = os.path.join(root_path, 'data', 'tests', 'integrationtests', json_name)
    json_content = open(json_path, encoding="utf-8")
    json_objects = json.load(json_content)

    # Adjust number if it is different.
    if number > len(json_objects):
        number = len(json_objects)
    send_data = []

    # Add each object.
    for i in range(number):
        if rng:
            send_data.append(json.dumps(random.choice(json_objects)))
        else:
            send_data.append(json.dumps(json_objects[i]))

    return send_data
