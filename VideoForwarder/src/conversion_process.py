"""File that creates the subprocess for the ffmpeg conversion.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from subprocess import Popen


def get_conversion_process(url, audio, root, stream_options):
    """Gets the ffmpeg conversion command for the camera stream that can be started later on.

    Args:
        url (str): Url of the camera
        audio (bool): Whether audio is included in the stream or not
        root (str): Path to files where the camera stream should be put
        stream_options (StreamOptions): object containing information on how to process the stream

    Returns:
        SubProcess: ffmpeg subprocess with the correct parameters
    """

    index = 0
    maps = []
    conversions = []
    stream_map = []

    # Options for the low stream quality.
    if stream_options.low:
        maps.extend(['-map', '0:0', '-map', '0:1'] if audio else ['-map', '0:0'])
        conversions.extend([
            f'-vf:v:{index}', "scale='if(lt(iw,ih),360,-2)':'if(lt(iw,ih),-2,360)'", f'-c:v:{index}', stream_options.encoding,
            f'-b:v:{index}', '800k', '-maxrate', '900k', '-bufsize', '1200k'
        ])  # 360p - Low bit-rate Stream
        stream_map.append(f'v:{index},a:{index}' if audio else f'v:{index}')
        index += 1

    # Medium stream quality.
    if stream_options.medium:
        maps.extend(['-map', '0:0', '-map', '0:1'] if audio else ['-map', '0:0'])
        conversions.extend([
            f'-vf:v:{index}', "scale='if(lt(iw,ih),420,trunc(oh*a/2)*2)':'if(lt(iw,ih),trunc(ow/a/2)*2,420)'", f'-c:v:{index}', stream_options.encoding,
            f'-b:v:{index}', '1425k', '-maxrate', '1600k', '-bufsize', '2138k'
        ])  # 420p - Medium bit-rate Stream
        stream_map.append(f'v:{index},a:{index}' if audio else f'v:{index}')
        index += 1

    # High stream quality.
    if stream_options.high:
        maps.extend(['-map', '0:0', '-map', '0:1'] if audio else ['-map', '0:0'])
        conversions.extend([
            f'-vf:v:{index}', "scale='if(lt(iw,ih),720,trunc(oh*a/2)*2)':'if(lt(iw,ih),trunc(ow/a/2)*2,720)'", f'-c:v:{index}', stream_options.encoding,
            f'-b:v:{index}', '2850k', '-maxrate', '3200k', '-bufsize', '4275k'
        ])  # 720p - High bit-rate Stream
        stream_map.append(f'v:{index},a:{index}' if audio else f'v:{index}')

    # Create the command to start ffmpeg with.
    # See https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new.
    command = [
        # Ffmpeg configurations.
        'ffmpeg', '-loglevel', 'fatal', '-i', url,
        # Create 3 variances of video + audio stream.
        *maps,
        '-profile:v', 'main', '-crf', '24', '-force_key_frames', 'expr:gte(t,n_forced*2)',
        '-sc_threshold', '0', '-g', '24', '-muxdelay', '0', '-keyint_min', '24',
        *(['-c:a', 'aac', '-ar', '48000'] if audio else []),
        # Set common properties of the video variances.
        *conversions,
        *(['-c:a', 'copy'] if audio else []),  # Copy original audio to the video variances.
        '-var_stream_map', (' '.join(stream_map)),
        # Create the master playlist.
        '-master_pl_name', 'stream.m3u8',
        # HLS flags and segment properties.
        '-hls_time', stream_options.segment_size, '-hls_list_size', stream_options.segment_amount, '-hls_flags',
        'delete_segments', '-start_number', '1',
        # Url.
        f'{root}/stream_V%v.m3u8'
    ]

    # Return the subprocess containing the ffmpeg command.
    return Popen(command)
