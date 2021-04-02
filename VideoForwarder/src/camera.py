# Object to store camera stream information in
class Camera:
    def __init__(self, ip, audio):
        self.ip = ip
        self.conversion = None
        self.callback = None
        self.audio = audio
