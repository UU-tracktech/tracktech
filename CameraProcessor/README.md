[![coverage report](https://https://git.science.uu.nl/e.w.j.bangma/tracktech/badges/SPC-285_Analyze_Code_Coverage/coverage.svg)](https://https://git.science.uu.nl/e.w.j.bangma/tracktech/commits/SPC-285_Analyze_Code_Coverage)

# Running the application
Running the app locally:

Installing python dependencies:
Download [python 3.8] and install the dependencies in requirements.txt in the base Camera Processor directory with 
```pip install -r requirements.txt```

Then, if you have [cuDNN 7.6.5] (for which you have to join membership) for [CUDA 10.1] installed on your computer 
(once again, NVIDIA only), you should be able to locally run main.py in the src directory.
This will run the YOLOv5 detection algorithm.


Dependencies install
```
pip install -r requirements.txt
```

##### Running in Docker. 
If you really want to be able to run it with GPU, it is a lot of hassle and not recommended for the average user.
Windows insider program slows down speed of pc a lot. Please ask Max or Gerard to verify if it is worth it.

1. GPU-enabled (Not recommended):
   1. You need an NVIDIA GPU that supports CUDA
   2. Follow the [nvidia install guide] step-by-step to expose your GPU to the docker container.
   3. Run rebuild.bat to build the container.
   4. Check the logs of your docker container in Docker Desktop to see if it is working properly.
2. GPU-disabled (can't run GPU code, only start container):
   1. Comment out the line ```CMD ["python3.8", "main.py"]``` in the Dockerfile.
   2. Replace the line ```docker run -t -d --gpus all --name %containerName% %imageName%``` by 
   ```docker run -t -d --name %containerName% %imageName%``` in the rebuild.bat file and run it.
   3. Now, you should be able to at least start the container. You will not be able to run any code, however.

[python 3.8]: https://www.python.org/downloads/release/python-380/
[tensorflow compatability]: https://www.tensorflow.org/install/source#gpu
[nvidia install guide]: https://docs.nvidia.com/cuda/wsl-user-guide/index.html
[CUDA 10.1]: https://developer.nvidia.com/cuda-10.1-download-archive-base
[cuDNN 7.6.5]: https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/production/10.1_20191031/cudnn-10.1-windows10-x64-v7.6.5.32.zip

# Pylint with PyCharm

We use Pylint for python code quality assurance

## Installation:

Input following command terminal:
```
pip install pylint
```

Install the PyCharm plugin:

`Control+Alt+S` to open PyCharm settings

Navigate to `Settings>Plugins`

Search for `pylint`

Install Pylint plugin

### Settings:

`Control+Alt+S` to open PyCharm settings

Navigate to `Settings>Other Settings>Pylint`

Set up link to Pylint and test settings.

Select the path to pylintrc (should be at root of project)

Click apply.

### Live linting while developing:

Nevigate to `Edtior>Inspections>Pylint`

Check `Pylint real-time scan`

### Ignoring folders from linting:

Mark desired folder as Excluded in PyCharm. (for local development)

Add folder name to `ignore=` in `pylintrc` (for CI pipeline)
