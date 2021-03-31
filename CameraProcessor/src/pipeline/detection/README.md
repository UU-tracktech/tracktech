## Input of detection
DetectionObj
  * int: Frame nr
  * DateTime: TimeStamp
  * Frame: Frame itself
  * [BoundingBox]: [ ]

## Output of detection
DetectionObj
  * int: Frame nr
  * DateTime: TimeStamp
  * Frame: Frame itself
  * [BoundingBox]: Boxes of detected objects

BoundingBox:
  * int: Identifier
  * Rectangle: (x1, y1, x2, y2)
  * FeatureObj: TBD
  * str: Classification (f.e. "Person")
  * float: Certainty
