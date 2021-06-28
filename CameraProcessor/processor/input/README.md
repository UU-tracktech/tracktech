# Input

The input is responsible for creating a matching way in which streams or multiple frames get served as separate frames.
The method and underlying functionality of these implementations get covered up by using the superclass: [icapture.py](icapture.py).

The ICapture class contains the following methods that have to get implemented by a subclass:
  - opened()
  - close()
  - get_next_frame()

If these get implemented correctly, the internal functionality does not behave any different from another.
Here a brief overview of the existing implementations.

### CamCapture
The [CamCapture](cam_capture.py) is for using a webcam on the device which runs the code.
This one will not work inside a docker container.

### HlsCapture
The [HlsCapture](hls_capture.py) uses an HLS URL of any HLS stream, and it will start a separate thread that creates an OpenCV capture object 
and reads frames at a constant rate adapted to the fps of the stream.
To synchronise the HLS stream from the video forwarder component (OpenCV does not let us read the header) another request is sent to the forwarder to retrieve the timestamp inside the stream header. This is used for the initial sync. 
After startup, the only synchronisation is done after a disconnect.

Note: Be sure to close this capture when it is not in use anymore since otherwise, the separate thread can cause issues when 
closing down the application

### ImageCapture
The [ImageCapture](image_capture.py) serves as a folder filled with image files.
It only requires the directory path and will play all images inside in sorted order.

[Here](https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html?highlight=imread#imwrite) are the supported image formats listed.

### VideoCapture
The [VideoCapture](video_capture.py) loads a video file and separates it into frames.
This capture is beneficial for the verification of the detection/tracking algorithm.

[Here](https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html?highlight=imread#videocapture-videocapture) is a list of video formats supported.
It says only .avi files are supported. It also runs .mp4, so the documentation does not list everything.
