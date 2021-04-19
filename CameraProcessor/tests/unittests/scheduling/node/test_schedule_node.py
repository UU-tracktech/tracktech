"""Import pytest and schedule_node.py for testing.

"""
import pytest
import processor.scheduling.node.schedule_node as schedule_node


# pylint: disable=attribute-defined-outside-init
class TestNode():
    """Tests bounding_box.py.
    """

    # Setup
    def setup_method(self):
        """Setup method for testing.

        """
        self.first_arg = 'first arg'

    def test_inode_reset(self):
        """Tests the functionality of INode: reset().

        """
        with pytest.raises(Exception):
            assert schedule_node.INode.reset(self.first_arg)

    def test_inode_executable(self):
        """Tests the functionality of INode: executable().

        """
        with pytest.raises(Exception):
            assert schedule_node.INode.executable(self.first_arg)

    def test_inode_execute(self):
        """Tests the functionality of INode: execute().

        """
        with pytest.raises(Exception):
            assert schedule_node.INode.execute(self.first_arg, notify=None)

    def test_inode_assign(self):
        """Tests the functionality of INode: assign().

        """
        with pytest.raises(Exception):
            assert schedule_node.INode.assign(self.first_arg, object, 0)

    def test_schedule_inode_reset(self):
        """Tests the functionality of Schedule(INode): reset().

        """
        with pytest.raises(Exception):
            assert schedule_node.INode.reset(self.first_arg)

    def test_schedule_inode_executable(self):
        """Tests the functionality of Schedule(INode): executable().

        """
        with pytest.raises(Exception):
            assert schedule_node.INode.executable(self.first_arg)

    def test_schedule_inode_execute(self):
        """Tests the functionality of Schedule(INode): execute().

        """
        with pytest.raises(Exception):
            assert schedule_node.INode.execute(self.first_arg, notify=None)

    def test_schedule_inode_assign(self):
        """Tests the functionality of Schedule(INode): assign().

        """
        with pytest.raises(Exception):
            assert schedule_node.INode.assign(self.first_arg, object, 0)


if __name__ == '__main__':
    pytest.main(TestNode)
