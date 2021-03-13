from queue import Queue


from scheduling.node.schedule_node import INode


class Scheduler:
    """Sequential scheduler executing a starting node and all children of said node when they are ready for execution.

    Attributes:
        start_node: INode representing the initial input node, starting point of the graph.
        queue: a queue containing nodes to execute, initially contains start_node
            and other nodes are put in queue when ready.
    """

    def __init__(self, start_node: INode):
        """Inits Scheduler with a starting node that contains the graph and a queue to determine execution order.

        Args:
            start_node: INode representing the initial input node, starting point of the graph.
        """
        self.start_node = start_node

        self.queue = Queue()

    def schedule_graph(self, input_obj: object) -> None:
        """Executes an iteration on the graph.

        Assigns the input object to the start node and queue start node to start iteration.
        Loops over queue as long as the queue isn't empty.

        Args:
            input_obj: object passed to the starting node to start an iteration.

        Raises:
            Exception: a node in the queue wasn't executable.
        """
        self.start_node.assign(input_obj, 0)

        self.queue.put(self.start_node)

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
            self.queue.put(node)


if __name__ == '__main__':
    from scheduling.plan.example_plan import schedule_input_node

    scheduler = Scheduler(schedule_input_node)
    scheduler.schedule_graph("test")

    curr_node = schedule_input_node
    while len(curr_node.out_nodes) > 0:
        curr_node = curr_node.out_nodes[0][0]
    print(curr_node.component.out)
