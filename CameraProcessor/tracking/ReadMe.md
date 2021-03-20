# Input of tracking
### DetectionObj:
  * int: Frame nr
  * DateTime: TimeStamp
  * Frame: Frame itself
  * [BoundingBox]\: Boxes of detected objects

### BoundingBox:
  * int: Identifier
  * Rectangle: (x1, y1, x2, y2)
  * FeatureObj: TBD
  * str: Classification (f.e. "Person")
  * float: Certainty

# Output of tracking
### TrackingObj:
  * int: Frame nr
  * Frame: Frame itself
  * [FeatureMap]\: Feature maps of tracked subjects  
  * [BoundingBox]\: Boxes of tracked objects
  * [BoundingBox]\: Boxes from detection phase

### BoundingBox:
  * int: Identifier
  * Rectangle: (x1, y1, x2, y2)
  * FeatureMap: FeatureMap
  * str: Classification (f.e. "Person")
  * float: Certainty
