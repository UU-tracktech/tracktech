import os

base = 'C:/Users/liyeu/Desktop/KI/master'
f = open(base + '.txt', "w+")
f.write(f'#EXTM3U\r\n#EXT-X-VERSION:3\r\n#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360\r\ncam1_360p.m3u8\r\n#EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=842x480\r\ncam1_480p.m3u8\r\n#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1280x720\r\ncam1_720p.m3u8\r\n#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080\r\ncam1_1080p.m3u8')
os.rename(base + '.txt', 'C:/Users/liyeu/Desktop/KI/master.m3u8')