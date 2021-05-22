"""Defines node class for scheduler with its connections to other nodes

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import numpy as np
from processor.scheduling.node.inode import INode


class ScheduleNode(INode):
    """Schedule node used by scheduler to schedule and ensure a minimum required order of execution.

    Arguments:
        input_count (int): total amount of arguments necessary to execute the component.
        out_nodes ([(INode, int)]): tuples of nodes in the next layer together with argument index
        to push argument to.
        component (IComponent): component to execute once the scheduler calls the node
        (all needed arguments should be ready).
        needed_args (int): amount of arguments still needed to execute the component.
        arguments (np.array): array of all arguments provided so far.
    """

    def __init__(self, input_count, out_nodes, component):
        """Inits ScheduleNode with information about the next layer and the component to execute.

        Args:
            input_count (int): total amount of arguments necessary to execute the component.
            out_nodes ([(INode, int)]): tuples of nodes in the next layer together with argument index
            to push argument to.
            component (IComponent): component to execute once the scheduler calls the node
            (all needed arguments should be ready).
        """
        self.input_count = input_count
        self.out_nodes = out_nodes
        self.component = component

        self.needed_args = self.input_count
        self.arguments = np.empty(self.needed_args, dtype=object)

    def reset(self):
        """Resets the node for the next iteration.

        Empties arguments array and resets amount of needed arguments.
        """
        self.needed_args = self.input_count

        # Keeping the numpy array and only emptying would be preferred
        self.arguments = np.empty(self.needed_args, dtype=object)

    def executable(self):
        """Checks whether all arguments needed for execution are provided.

        Returns:
            bool: true if all arguments have been provided, false otherwise.
        """
        return self.needed_args <= 0

    def execute(self, notify):
        """Execute the component and pass output to next layer.

        Executes the component with the previously provided arguments in the arguments array.
        Throws error if node isn't executable.
        Pass the output of the component to nodes in the next layer
        by looping over all nodes in the next layer.
        Notify the scheduler of nodes that can now be executed since
        the contained component has been run.
        Reset the node.

        Args:
            notify (Callable[[List[INode]], None]): function to pass nodes to that can be
                executed after the component was executed.

        Raises:
            Exception: node is not ready to execute.
        """
        if not self.executable():
            raise Exception("Can't call function without the function's arguments being complete")

        # Fold arguments into components work function and receive component output.
        out = self.component.execute_component()(*self.arguments)

        ready_nodes = []

        # Assign output of component to all nodes in the next layer.
        for (node, arg_nr) in self.out_nodes:
            node.assign(out, arg_nr)

            # Check if node is ready after previous assign was performed.
            if node.executable():
                ready_nodes.append(node)

        # Notify the scheduler of all nodes that can now be executed.
        notify(ready_nodes)

        # Reset node state for next iteration.
        self.reset()

    def assign(self, arg, arg_nr):
        """Store argument for later component execution in the arguments array.

        Args:
            arg (object): argument to store for when the component is executed.
            arg_nr (int): index at which the argument is stored in the arguments array.

        Raises:
            IndexError: wrong index for the argument was given.
            Exception: argument is provided twice, existing argument would be overwritten.
        """
        if len(self.arguments) <= arg_nr:
            raise IndexError("Index %s too large for arguments array with size %x" %
                             (arg_nr, len(self.arguments)))

        # Ensure previously supplied argument isn't overwritten.
        if self.arguments[arg_nr] is None:
            self.arguments[arg_nr] = arg

            self.needed_args -= 1
        else:
            raise Exception("Argument should only be provided once by the scheduler, "
                            "this indicates unnecessary execution by the scheduler")
