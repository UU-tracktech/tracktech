
# Training the algorithms

The following will describe how to train a model for the detection stage and the re-identification stage.


## Run Locally

Clone the project

```bash
git clone https://github.com/UU-tracktech/tracktech.git
```

Go to the project directory.

```bash
cd <root-of-project>
```

Install dependencies (local)

```bash
npm install Interface/react
pip install CameraProcessor/requirements.txt
pip install CameraProcessor/requirements-reid.txt
pip install CameraProcessor/requirements-gpu.txt
pip install CameraProcessor/requirements-test.txt
pip install CameraProcessor/processor/pipeline/detection/yolov5/requirements.txt
pip install CameraProcessor/processor/pipeline/detection/yolor/requirements.txt
pip install CameraProcessor/processor/pipeline/reidentification/torchreid/requirements.txt
pip install ProcessorOrchestrator/requirements.txt
pip install ProcessorOrchestrator/requirements-test.txt
pip install VideoForwarder/requirements.txt
pip install VideoForwarder/requirements-test.txt
```
OR

Install dependencies (Docker)
```bash
docker compose up
```

  
## Settings

To run the training, you need to set the following values (text below show the default values)

The user can change the settings in the `configs.ini` file in the `CameraProcessor` folder.

In addition, place the datasets you want to use in the `CameraProcessor/data/annnotated` folder.

### Detection:

#### Training Yolov5

```
[Training_Yolov5]
data = /data/coco128.yaml     # Location of the dataset, currently set to the COCO128 dataset.
cfg = /models/yolov5s.yaml    # Location of the model, currently set to the small Yolov5 model.
weights = \'\'                # Location of weights file, usually empty because that will be result of training.
batch-size = 4                # Batch size of training, should be set to 2-4 times your avaiable video RAM.
hyp = /data/hyp.scratch.yaml  # hyp file used for training.
```

#### Training Yolor

```
[Training_Yolor]
multi-gpu = False                  # Whether or not to use multiple GPU for training. Requires multiple GPU when set to True.
data = /data/coco.yaml             # Location of the dataset, currently set to the COCO dataset.
cfg = /cfg/yolor_p6.cfg            # Location of the config file for training.
img = 1280 1280                    # Image dimensions to train on.
device = 0                         # GPU device used for training.
name = yolor_p6                    # Output filename.
weights = \'\'                     # Location of weights file, usually empty because that will be result of training.
batch-size = 4                     # Batch size of training, should be set to 2-4 times your avaiable video RAM.
hyp = /data/hyp.scratch.1280.yaml  # hyp file used for training.
epochs = 300                       # Number of epochs to run for training.
```

### Re-Identification:

#### Training Torchreid

```
[Training_Torchreid]
root = ../../../data/annotated  # Dataset location.
sources = market1501            # Dataset name.
targets = market1501            # Dataset to train on.
width = 256                     # Height dimension of input pictures.
height = 128                    # Width dimension of input pictures.
batch_size_train = 32           # Batch size to use during training.
batch_size_test = 100           # Batch size to use during testing.
model = resnet50                # Model to use during training.
save_dir = log/resnet50         # Directory to save results.
max_epoch = 60                  # Number of epochs.
eval_freq = 10                  # Evalution frequency.
print_freq = 10                 # Print frequency.
```

#### Training Fastreid

```
[Training_Fastreid]
num_gpus = 1                                        # Number of gpus to use.
config_file = /configs/Market1501/bagtricks_R50.yml # Config file inside FastReid
model_device = cuda                                 # Type of gpu
device_number = 0                                   # Device number.
```

## Running the training

Run the following from Powershell (Windows) or Terminal (Unix):

### Detection

Set the training mode in `configs.ini` in CameraProcessor to the desired value:

```bash
[Training]
# mode values: yolov5, yolor
mode = yolor      # This value determines the training mode.
file = /train.py
```

#### Yolov5

With mode in `configs.ini` set to `yolov5`:

```bash
cd CameraProcessor/processor/training/detection/
python3 train.py
```

#### Yolor

With mode in `configs.ini` set to `yolor`:

```bash
cd CameraProcessor/processor/training/detection/
python3 train.py
```

### Re-Identification

#### Torchreid

```bash
cd CameraProcessor/processor/training/reidentification/
python3 train.py
```

#### Fastreid

```bash
cd <location-of-root>/CameraProcessor/processor/pipeline/reidentification/Fastreid
export FASTREID_DATASETS=../../../../data/annotated/Market1501/
python3 tools/train_net.py --config-file ./configs/Market1501/bagtricks_R50.yml MODEL.DEVICE "cuda:0"
```

## Determining the accuracy

### Detection

Set the Accuracy mode in `configs.ini` in CameraProcessor to the desired value:

```bash
[Accuracy]
# Detection algorithm to use for accuracy. Values: yolov5, yolor
detector = yolov5
# Re-identification algorithm to use for accuracy. Values: torchreid, fastreid
reid = torchreid
```

#### Yolov5

With detector in `configs.ini` set to `yolov5`:

```bash
cd CameraProcessor/processor/training/detection/
python3 accuracy_object.py
```

#### Yolor

With detector in `configs.ini` set to `yolor`:

```bash
cd CameraProcessor/processor/training/detection/
python3 accuracy_object.py
```

### Re-Identification

#### Torchreid

With reid in `configs.ini` set to `torchreid`:

```bash
cd CameraProcessor/processor/training/reidentification/
python3 accuracy_object.py
```

#### Fastreid

Due to limitations, FastReid has to be directly called to evaluate using the command line:

```bash
cd <location-of-root>/CameraProcessor/processor/pipeline/reidentification/Fastreid
export FASTREID_DATASETS=../../../../data/annotated/Market1501/
python3 tools/train_net.py --config-file ./configs/Market1501/bagtricks_R50.yml ---eval-only MODEL.WEIGHTS /path/to/weight-file MODEL.DEVICE "cuda:0"
```
  

## FAQ

#### Why is there no training for tracking?

Tracking uses either Sort or Sort_OH. Both of these algorithms are not based not a neural network, and thus the user cannot train the tracking stage. These algorithms solely rely on the detection stages' result. To improve tracking, please try to improve detection performance.

#### I'm getting paging file size errors on Windows. How do I fix this?

This error means that Windows does not have sufficient disk space for a paging file during the training. Either create more disk space by removing other files from the disk or consider running the training on a Unix based system.

#### The resulting models from training give poor performance. How do I fix this?

Consider running training on a larger part of the dataset and for more epochs. Generally speaking, the larger the dataset used and the longer trained, the better the resulting model.

#### I'm missing a dependency. Where can I find it?

Try installing the package as follows:

```bash
pip install <name-of-package>
```

#### The program cannot find my datasets. Where do I store them?

All datasets should be located in `<root-to-folder>/CameraProcessor/data/annotated/<name-of-dataset>/`

For example, when using the Market1501 and COCO datasets, the folder structure might look something like this:

```
.
└──CameraProcessor
   └──data
      └──annotated
         ├──COCO
         │  ├──annotations
         │  └──images
         └──market1501
            └──Market-1501-v15.09.15
               ├──bounding_box_test
               ├──bounding_box_train
               ├──gt_bbox
               ├──gt_query
               ├──query
               └──readme.txt
```

Re-identification on fastreid is an exception: it requires the dataset to be located next to the `accuracy_object.py`
file in a folder names `datasets`.

#### I want to train with custom data. Is this possible?

Yes, as long as the data is in similar format as one of the supported datasets.
