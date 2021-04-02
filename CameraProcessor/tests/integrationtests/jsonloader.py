import json


def load_data(datatype):
    """Load a JSON test data file of chosen type.

    Args:
        A string, which is one of these options: {'boundingBoxes', 'start', 'stop', 'featureMap'}

    Returns:
        A dictionary of test data of the chosen JSON message type
    """
    switcher = {
        'boundingBoxes': 'boxes',
        'start': 'stopstart',
        'stop': 'stopstart',
        'featureMap': 'featuremaps'
    }
    filename = switcher.get(datatype)
    if filename is None:
        raise NameError('The JSON object requested is not in scope.')
    else:
        f = open(f'testdata/{filename}.json')
        return json.load(f)
