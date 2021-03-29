# ICapture enforces implementation fo the following methods
class ICapture:
    # Check if stream is stopped
    def opened(self) -> bool:
        raise NotImplementedError('stopped method not implemented')

    # Closes the capture object
    def close(self) -> None:
        raise NotImplementedError('No close defined for the capture')

    # Gets the next frame
    def get_next_frame(self):
        raise NotImplementedError('No implementation for getting next frame')
