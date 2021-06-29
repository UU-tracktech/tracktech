# Tracking  
The tracking package contains the [tracker interface](itracker.py), 
Furthermore, all currently implemented tracking algorithms with their associated runner implementation.
  
## tracking.itracker  

The [ITracker](itracker.py) class is used as an interface which all tracking runners must implement.
It enforces the implementation of one method, `track(frame_obj, det_obj)`, which takes a 
[FrameObj](../../data_object/frame_obj.py) and [BoundingBoxes](../../data_object/bounding_boxes.py) as input, 
and returning all objects tracked in the current frame as [BoundingBoxes](../../data_object/bounding_boxes.py).

## tracking.sort_tracker  

The [sort_tracker.py](sort_tracker.py) is the runner for the [SORT](https://github.com/abewley/sort) tracking algorithm (more on SORT later).
The runner does a conversion of all detections in the current frame, updates the tracker with these detections 
and gets all trackers (old and new) in the current frame returning these trackers as [BoundingBoxes](../../data_object/bounding_boxes.py).

### Preparation of detections

The detections are all [BoundingBoxes](../../data_object/bounding_boxes.py) in the current frame.
Each [BoundingBox](../../data_object/bounding_box.py) gets converted to a list `[x1, y1, x2, y2, confidence]`.
All these lists get put into a single NumPy array.

### Retrieval of trackers

The SORT tracker returns all old and new trackers in the current frame. These get converted back to [BoundingBoxes](../../data_object/bounding_boxes.py).
An old tracker is a tracker which is an already tracked person that was recognized again.
A new tracker is a tracker which has just been added after the minimal amount of hits was reached. 
(amount of frames the person was recognized as being the same object).

### SORT tracking

[SORT](https://github.com/abewley/sort) stands for Simple Online and Realtime Tracking and is an algorithm for 2D multiple objects tracking in video sequences.
It only uses past and present frames for tracking and forgets about objects that have not been detected for too long.
It uses the Kalman filter to determine if a tracker from a previous frame is the same object as a detection from the current frame.
SORT uses the distance, velocity, time and, colour composition to determine the tracker associated with an object. 
