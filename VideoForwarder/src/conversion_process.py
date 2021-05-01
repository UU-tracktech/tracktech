"""File that creates teh subprocess for the ffmpeg conversion

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

from subprocess import Popen

from utils import get_stream_variables


def get_conversion_process(ip_address, audio, camera, root):
    """Gets the ffmpeg conversion command for the camera stream that can be started later on

    Args:
        ip_address (str): Ip address of the camera
        audio (bool): Whether audio is included in the stream or not
        camera (Camera): The camera object containing
        root (str): Path to files where the camera stream should be put

    Returns:
        SubProcess: ffmpeg subprocess with the correct parameters
    """
    # Get variables from environment
    segment_size, segment_amount, encoding, _, _ = get_stream_variables()

    # Default value when audio is not included
    maps = ['-map', '0:0', '-map', '0:0', '-map', '0:0']
    caarg = []
    copy = []
    stream_map = 'v:0 v:1 v:2'

    # Audio enabled
    if audio:
        maps = ['-map', '0:0', '-map', '0:1', '-map', '0:0', '-map', '0:1', '-map', '0:0', '-map', '0:1']
        caarg = ['-c:a', 'aac', '-ar', '48000']
        copy = ['-c:a', 'copy']
        stream_map = 'v:0,a:0 v:1,a:1 v:2,a:2'

    # see https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new
    # Returns the opened path
    return Popen([
        # ffmpeg configurations
        'ffmpeg', '-loglevel', 'fatal', '-rtsp_transport', 'tcp', '-i', ip_address,
        # Create 3 variances of video + audio stream
        *maps,
        '-profile:v', 'main', '-crf', '24', '-force_key_frames', 'expr:gte(t,n_forced*2)',
        '-sc_threshold', '0', '-g', '24', '-muxdelay', '0', '-keyint_min', '24',
        *caarg,
        # Set common properties of the video variances
        '-s:v:0', '640x360', '-c:v:0', encoding, '-b:v:0', '800k', '-maxrate',
        '900k', '-bufsize', '1200k',  # 360p - Low bit-rate Stream
        '-s:v:1', '854x480', '-c:v:1', encoding, '-b:v:1', '1425k', '-maxrate',
        '1600k', '-bufsize', '2138k',  # 420p - Medium bit-rate Stream
        '-s:v:2', '1280x720', '-c:v:2', encoding, '-b:v:2', '2850k', '-maxrate',
        '3200k', '-bufsize', '4275k',  # 720p - High bit-rate Stream
        *copy,  # Copy original audio to the video variances
        '-var_stream_map', stream_map,
        # Create the master playlist
        '-master_pl_name', f'{camera}.m3u8',
        # HLS flags and segment properties
        '-hls_time', segment_size, '-hls_list_size', segment_amount, '-hls_flags',
        'delete_segments', '-start_number', '1',
        # Url
        f'{root}/{camera}_V%v.m3u8'
    ])
