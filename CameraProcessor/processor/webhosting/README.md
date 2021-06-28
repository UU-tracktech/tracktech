# Webhosting

The content of this folder uses the [Tornado](https://www.tornadoweb.org/en/stable/) library for communication with the outside world.

These handlers are for Docker debugging and remote verification purposes.
This creates an HTTP server that can be connected to see the output of a single Camera Processor online without having to boot up the entire system.
- [html_page_handler.py](html_page_handler.py): Serves the webpage in which the stream is visible
- [stream_handler.py](stream_handler.py): Serves the individual frames to the WebClient

### Hosting website

Tornado is also used for remote verification and to visually verify results in Docker. When the detection and tracking are done,
the output image can be served to a WebClient. The HTML page of the website is stored inside the [webpage](../../webpage) folder
and given by the [html_page_handler.py](html_page_handler.py).

After the HTML page is loaded, the stream gets created, and the process_stream loop starts inside the [stream_handler.py](stream_handler.py).
This class contains the serving logic for when the frame is processed. Every 0.1 seconds, the processed frames get flushed so the client can retrieve the images. 

The [stream_handler.py](stream_handler.py) implements a RequestHandler, which starts a coroutine that contains the main loop of the application.
Because of the coroutine, the get does not consist of a single GET command, but instead, it repeatedly requests the images from the stream.
