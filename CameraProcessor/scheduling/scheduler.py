from queue import Queue


from scheduling.node.schedule_node import INode


class Scheduler:
    """Sequential scheduler executing a starting node and all children of said node when they are ready for execution.

    Attributes:
        start_node: INode representing the initial input node, starting point of the graph.
        queue: a queue containing nodes to execute, initially contains start_node
            and other nodes are put in queue when ready.
        queued: set of all nodes that have been queued in the current iteration.
    """

    def __init__(self, start_node: INode):
        """Inits Scheduler with a starting node that contains the graph and a queue to determine execution order.

        Args:
            start_node: INode representing the initial input node, starting point of the graph.
        """
        self.start_node = start_node

        self.queue = Queue()
        self.queued: set = set()

    def schedule_graph(self, input_obj: object) -> None:
        """Executes an iteration on the graph.

        Assigns the input object to the start node and queue start node to start iteration.
        Loops over queue as long as the queue isn't empty.

        Args:
            input_obj: object passed to the starting node to start an iteration.

        Raises:
            Exception: a node in the queue wasn't executable.
        """
        self.queued: set = set()

        self.start_node.assign(input_obj, 0)

        self.push(self.start_node)

        # Loop over queue until there are no more nodes to execute (queue is empty).
        while not self.queue.empty():
            node = self.queue.get()

            if node.executable():
                node.execute(self.notify)
            else:
                raise Exception("Node in queue should be executable")

    def notify(self, ready_nodes: list[INode]) -> None:
        """Queues nodes that are ready to be executed.

        Args:
            ready_nodes: nodes to queue.
        """
        for node in ready_nodes:
            self.push(node)

    def push(self, node: INode):
        """Push node on the queue when it hasn't entered the queue yet in the current iteration.

        Args:
            node: node to put in queue when it is its first occurrence this iteration.
        """
        if id(node) not in self.queued:
            self.queue.put(node)
            self.queued.add(id(node))
