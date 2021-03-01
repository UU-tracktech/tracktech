**Still very WIP**

## Input of tracking
DetectionObj
  * int: Frame nr
  * DateTime: TimeStamp
  * Frame: Frame itself
  * [BoundingBox]: Boxes of detected objects

## Output of tracking
TrackingObj:
  * DetectionObj
  * [TrackingFeature]: Sortof FeatureMap
    
    
HTTPJSON:
  * [FeatureMap]: Featuremap of tracked objects