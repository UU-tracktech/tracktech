# training/detection

## Training a model

Change working directory to ```~/CameraProcessor/processor/pipeline/detection/yolov5``` and run the follwing command

```
python train.py --data coco128.yaml --cfg yolov5s.yaml --weights '' --batch-size 4
```

- ```--data``` defines the location of the dataset

- ```--cfg``` defines the config file for reading the weights from the dataset

- ```--weights``` defines the weights to use for training

- ```--batch-size``` defines the batch size to use. This can be set to 2-4 times your GPU memory.

## accuracy_object.py

```python
import processor.training.detection.accuracy_object
```

[accuracy_object.py](accuracy_object.py) parses the information needed to run accuracy functionality and converts it
into a format that is supported by the accuracy class.
It furthermore can generate precision-recall graphs of the results.

`read_config(self)` parses the `config.ini` file.

`parse_into_file(self)` parses a config file and extracts the frame count and image dimensions.
It automatically determines the delimiters.

`parse_boxes(self, boxes_to_parse)` takes a list of bounding boxes and parses them to a format supported
by the `PODM` library.

`read_boxes(self, path_to_boxes)` uses the `PreAnnotations` to load a list of bounding boxes from a file
and parses the bounding boxes through the `parse_boxes` function, before returning the result.

`detect(self)` retrieves the accuracy of detections from a folder prespecified in the `__init__`.
It prints the true positives `tp`, false positives `fp`, false negatives `fns` and mean average precision `mAP`.

`draw_pr_plot(self, result)` draws a precision recall graph from a single `result` using the `PODM` library.
The result is an image displaying the graph.

`draw_all_pr_plots(self)` runs the `draw_pr_plot` function for every class.

## train.py

```python
import processor.training.detection.train
```

[train.py](train.py)

