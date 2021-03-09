from queue import Queue


from scheduling.node.schedule_node import INode


class Scheduler:
    def __init__(self, start_node: INode):
        self.start_node = start_node

        self.queue = Queue()

    def schedule_graph(self, input_obj: object) -> None:
        self.start_node.assign(input_obj, 0)

        self.queue.put(self.start_node)

        while not self.queue.empty():
            node = self.queue.get()

            if node.executable():
                node.execute(self.notify)
            else:
                raise Exception("Node in queue should be executable")

    def notify(self, ready_nodes: list[INode]) -> None:
        for node in ready_nodes:
            self.queue.put(node)
