# Forwarder

This component retrieves a webstream and converts it to an HLS stream. This HLS stream can then be consumed by the interface and processors.

## Quickstart

### Starting

#### Docker

Run the following command to startup the forwarder

```bash
docker run -p 80:80 --env CAMERA_URL={Stream url} --env CAMERA_AUDIO={Wether the stream contains audio} --env STREAM_LOW=true tracktech/forwarder
```

#### Local

Make sure python is installed and the repository is cloned install the dependencies using

```bash
pip install -r requirements.txt
pip install Auth-1.0.tar.gz
```

Set the CAMERA_URL, CAMERA_AUDIO, STREAM_LOW and STREAM_FOLDER environment variables to their desired values and set PYTHONPATH to the current directory.

Run the program

```bash
python src/main.py
```

The stream can then be accessed at `http://localhost/stream.m3u8`

### Environment variables

#### Camera

Required to specify

| Variable     | Description                                        |
| ------------ | -------------------------------------------------- |
| CAMERA_URL   | The video stream url of the camera                 |
| CAMERA_AUDIO | Whether the camera stream contains an audio stream |

#### Streaming

| Variable        | Description                                                             | Default      |
| --------------- | ----------------------------------------------------------------------- | ------------ |
| SEGMENT_SIZE    | The size of a single segment in seconds                                 | 2            |
| SEGMENT_AMOUNT  | The amount of segments stored at once for a single stream               | 5            |
| REMOVE_DELAY    | The amount of seconds of inactivity before a stream is closed           | 60           |
| TIMEOUT_DELAY   | The amount of seconds to wait for a stream to open and produce segments | 30           |
| STREAM_ENCODING | The encoder used to encode the stream                                   | libx264      |
| STREAM_FOLDER   | The folder in which the hls stream files are stored                     | /app/streams |
| STREAM_LOW      | use 'true' to enable a low quality stream                               | false        |
| STREAM_MEDIUM   | use 'true' to enable a medium quality stream                            | false        |
| STREAM_HIGH     | use 'true' to enable a high quality stream                              | false        |

#### SSL

If both are specified, ssl is enabled

| Variable | Description              |
| -------- | ------------------------ |
| SSL_CERT | The ssl certificate path |
| SSL_KEY  | The ssl key path         |

#### Authentication

| Variable    | Description                                     |
| ----------- | ----------------------------------------------- |
| PUBLIC_KEY  | The public key file to validate the tokens with |
| AUDIENCE    | The id of this client the token is meant for    |
| CLIENT_ROLE | The role to check for in the token              |

## Architecture

We use ffmpeg to pull the video stream and encode it to an HLS stream. This is a http based streaming protocol that allows adaptive bitrate streaming. We use tornado to serve the files and handle authentication, to match the rest of the project.

## Depencencies

### Software

- Python 3.8
- FFMPEG

### Packages

- Tornado (python)
- The Auth module

## Development

### Testing

In order to run the unit tests please run `docker-compose -f compose/docker-compose_test_unit.yml`
