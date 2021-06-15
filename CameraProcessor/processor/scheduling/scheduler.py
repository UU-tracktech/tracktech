"""Defines the scheduler class, is for executing tasks concurrently by creating node structure.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from queue import Queue


class Scheduler:
    """The sequential scheduler executing a starting node and all its children node when they are ready for execution.

    Attributes:
        start_node (INode): INode representing the initial input node, starting point of the graph.
    """

    def __init__(self, start_node):
        """Inits Scheduler with a starting node that contains the graph, and a queue to determine execution order.

        Args:
            start_node (INode): INode representing the initial input node, starting point of the graph.
        """
        self.start_node = start_node

        self.__queue = Queue()
        self.__queued = set()

    def schedule_graph(self, inputs, global_readonly):
        """Executes an iteration on the graph.

        Assigns the input object to the start node and queue start node to start iteration.
        Loops over queue as long as the queue isn't empty.

        Args:
            inputs ([object]): list of objects passed to the starting node to start an iteration.
            global_readonly (dict[str, object]): list of objects that can be used by all nodes,
                should never modify (use as readonly).

        Raises:
            Exception: a node in the queue wasn't executable.
        """
        self.__queued = set()

        # Assign inputs to initial/start node.
        for i, node_input in enumerate(inputs):
            self.start_node.assign(node_input, i)

        self.push(self.start_node)

        # Loop over queue until there are no more nodes to execute (queue is empty).
        while not self.__queue.empty():
            node = self.__queue.get()

            if node.executable():
                node.execute(self.notify, global_readonly)
            else:
                raise Exception("Node in queue should be executable")

    def notify(self, ready_nodes):
        """Queues nodes that are ready to be executed.

        Args:
            ready_nodes ([INode]): nodes to queue.
        """
        for node in ready_nodes:
            self.push(node)

    def push(self, node):
        """Push node on the queue when it hasn't entered the queue yet in the current iteration.

        Args:
            node (INode): node to put in queue when it is its first occurrence this iteration.
        """
        if id(node) not in self.__queued:
            self.__queue.put(node)
            self.__queued.add(id(node))

    @property
    def queue_size(self):
        """Get the size of the queue.

        Returns:
            int: size/length of the queue.
        """
        return self.__queue.qsize()
