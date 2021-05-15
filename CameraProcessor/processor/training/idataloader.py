class IDataloader:
    def __init__(self, file_path, nr_frames):
        self.file_path = file_path

        # Cannot contain negative amount of frames.
        if nr_frames < 0:
            raise AttributeError('Cannot have negative number of frames')
        self.nr_frames = nr_frames

        # Foreach frame create an empty list.
        self.boxes = [[] for _ in range(nr_frames)]

    def parse_file(self):
        """Parses a file into a BoundingBoxes object.

        Returns: a BoundingBoxes object.

        """
        raise NotImplementedError('parse file method not implemented')