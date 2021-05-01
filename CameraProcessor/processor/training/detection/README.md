## how to run training

Change working directory to ```~/CameraProcessor/processor/pipeline/detection/yolov5``` and run the follwing command

```
python train.py --data coco128.yaml --cfg yolov5s.yaml --weights '' --batch-size 4
```

```--data``` defines the location of the dataset

```--cfg``` defines the config file for reading the weights from the dataset

```--weights``` defines the weights to use for training

```--batch-size``` defines the batch size to use. This can be set to 2-4 times your GPU memory.