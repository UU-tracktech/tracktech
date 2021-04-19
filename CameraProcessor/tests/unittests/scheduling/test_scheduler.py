"""Import pytest and scheduler.py for testing.

"""
import pytest
import processor.scheduling.scheduler as scheduler


# pylint: disable=attribute-defined-outside-init
class TestScheduler():
    """Tests bounding_box.py.
    """

    # Setup
    def setup_method(self):
        """Setup method for testing.

        """
        self.data = scheduler
        self.start_node = self.data.INode
        self.queue = self.data.Queue
        self.scheduler = self.data.Scheduler

    def test_schedule_graph(self):
        """Tests the functionality of schedule_graph().

        """
        with pytest.raises(NotImplementedError):
            scheduler.Scheduler.schedule_graph(self, self.start_node.assign(self, object, 0))

    def test_notify(self):
        """Tests the functionality of notify().

        """
        with pytest.raises(NotImplementedError):
            scheduler.Scheduler.notify(self,
                                       [self.start_node.assign(self, object, 0),
                                       self.start_node.assign(self, object, 1)])

    def test_push(self):
        """Tests the functionality of push().

        """
        with pytest.raises(NotImplementedError):
            assert scheduler.Scheduler.push(self, self.start_node.assign(self, object, 0))


if __name__ == '__main__':
    pytest.main(TestScheduler)
