import json

def loadData(datatype):
    switcher={
        'boundingBoxes': 'boxes',
        'start': 'stopstart',
        'stop':'stopstart',
        'featureMap': 'featuremaps'
    }
    filename = switcher.get(datatype)
    if filename is None:
        raise NameError('The JSON object requested is not in scope.')
    else:
        f = open(f'testdata/{filename}.json')
        return json.load(f)