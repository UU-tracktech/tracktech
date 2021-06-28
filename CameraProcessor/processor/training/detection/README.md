# Training of Detection

This component trains the object detection component of the program. It uses object detection datasets such as the 
[COCO dataset](https://cocodataset.org/#home) to train for object detection.

## Training a model

Executing [train.py](train.py) starts the training of the detection model. It runs the command for the specified
training mode in the [configs file](../../../configs.ini):

### Training Yolov5:
```
python train.py --data coco128.yaml --cfg yolov5s.yaml --weights '' --hyp hyp.scratch.yaml --batch-size 4
```

- ```--data``` defines the location of the dataset.

- ```--cfg``` defines the config file for reading the weights from the dataset.

- ```--weights``` defines the weights to use for training.

- ```--hyp``` defines the hyp configuration for use for training.

- ```--batch-size``` defines the batch size to use. This can be set to 2-4 times the GPU's memory.

The values of these parameters can be configured in the [configs.ini](../../../configs.ini) file.

### Training Yolor:

Yolor also allows for multi-GPU training. This speeds up the training process significantly.

```
python train.py --batch-size 8 --img 1280 1280 --data coco.yaml --cfg cfg/yolor_p6.cfg --weights '' --device 0 --name yolor_p6 --hyp hyp.scratch.1280.yaml --epochs 300
```
- ```--multi-gpu``` defines whether or not to use multiple GPUs for training.

- ```--data``` defines the location of the dataset.

- ```--cfg``` defines the config file for reading the weights from the dataset.

- ```--weights``` defines the weights to use for training.

- ```--hyp``` defines the hyp configuration for use for training.

- ```--batch-size``` defines the batch size to use. This can be set to 2-4 times the GPU's memory.

- ```--img``` defines the image dimensions.

- ```--device``` defines what GPU top use.

- ```--name``` defines the name of the model resulting from training.

- ```--epochs``` defines how many iterations to train. More is better but takes longer.

The values of these parameters can be configured in the [configs.ini](../../../configs.ini) file.


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

`read_boxes(self, path_to_boxes)` uses the `PreAnnotations` to load a list of bounding boxes from a file and parses the bounding boxes through the `parse_boxes` function before returning the result.

`detect(self)` retrieves the accuracy of detections from a folder prespecified in the `__init__`.
It prints the true positives `tp`, false positives `fp`, false negatives `fns`, and mean average precision `mAP`.

`draw_pr_plot(self, result)` draws a precision-recall graph from a single `result` using the `PODM` library.
The result is an image displaying the graph.

`draw_all_pr_plots(self)` runs the `draw_pr_plot` function for every class.

## train.py

[train.py](train.py) runs the training of the detection model as explained in the
[first section](#training-a-model).

