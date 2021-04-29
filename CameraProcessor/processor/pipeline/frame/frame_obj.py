class FrameObj:
    def __init__(self, frame, timestamp):
        self.__frame = frame
        self.__timestamp = timestamp

    def get_frame(self):
        return self.__frame

    def get_timestamp(self):
        return self.__timestamp
