
# detection  
This folder contains our detector classes for the classification and detection of loose images or images taken from video streams. We have one base class, IDetector, from which other detectors inherit.   
  
## detection.idetector  
The IDetector class is an inheritable base class that implemented detectors inherit from. It has one public function inherited by every child class, `detect`, which takes `FrameObj` as parameter.  
### Input of `detect`  
```python  
from processor.data_object.frame_obj import FrameObj  
```  
The detection function takes a [`FrameObj`](processor.data_object.frame_obj.y) as parameter. This FrameObject holds an image to run detection on and a timestamp. The image is to be taken from a stream, with the timestamp usually included in the metadata of most types of video streams.  Pass as a parameter to the Detector of choice.   
  
More information on the use or construction of the object can be found in the [README](processor.data_object.README.md) instructions in the `data_object` folder.   
### Output of `detect`  
```python  
from processor.data_object.bounding_boxes import BoundingBoxes  
```  
The output of the detection stage is an object, [BoundingBoxes](processor.data_object.bounding_boxes.py), containing a list of [BoundingBox](processor.data_object.bounding_box.py) objects. These contain various information such as classification and certainty. The output of detection can be used directly for displaying the boxes on the image or used in subsequent processes such as tracking or re-identification.   
## detection.yolov5_runner  
```python  
from processor.pipeline.detection.yolov5_detector import Yolov5Detector  
```  
  
### Introduction  
[YOLOv5](https://github.com/ultralytics/yolov5) is a state-of-the-art detection algorithm released by [Ultralytics](https://github.com/ultralytics) in June 2020, with the latest build being from April 2021. It is based on the YOLO (You Only Look Once) networks originally developed by [Joseph Redmon](https://arxiv.org/pdf/1506.02640.pdf) in 2016. It was released mere months after [YOLOv4](https://arxiv.org/abs/2004.10934), which was developed by Alexey Bochkovskiym with no affiliation to Joseph Redmon (who had [stepped away](https://twitter.com/pjreddie/status/1230524770350817280) from the project after YOLOv2).  
  
Notably, the release of YOLOv5 came with some [controversy](https://blog.roboflow.com/yolov4-versus-yolov5/). To sum up, the name might be more of a market gimmick than an actual indication of improvement over the previous YOLOv4, and the [performance might not necessarily be better](https://medium.com/deelvin-machine-learning/yolov4-vs-yolov5-db1e0ac7962b).  
  
There are two reasons we opted to use YOLOv5 over the YOLOv4 repository by Alexey. Firstly, it is implemented in PyTorch, which allows for ease of use over the C/C++ implementation of YOLOv4. Secondly, the non-affiliated adaptions of YOLOv4/Darknet in Python frameworks (such as TensorFlow and PyTorch) left something to be desired in terms of readability.  
  
### Yolov5Detector  
  
The `Yolov5Detector` inherits from `IDetector`. It has an initialization that requires several parameters.  
* `config`: A section, in the form of a Python dict, of the `configs.ini` file located in the root. It contains configuration options and file paths to other needed elements such as the CNN weights file.   
* `filters`: Another section, also in the form of a Python dict, of the `configs.ini` file located in the root, this containing a single path to a file