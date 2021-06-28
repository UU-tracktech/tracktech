# Scheduling

There are many methods to achieve the tracking of subjects and objects 
over multiple cameras.
The method can be divided into several components.
Some of these components can be run in parallel since they do not need
anything from each other.
This parallelism can be hardcoded in the component itself, 
However, this is unfavourable since there are many methods to try.

A scheduling process that takes in a plan (graph) 
is better when trying multiple methods.
The scheduler is responsible for the execution of the nodes and can have extensions for parallelism and more built-in.
This prevents recoding previously made components when a new component
is added, or an existing component is updated.

## scheduling.scheduler

The scheduler [scheduler.py](scheduler.py) is a sequential scheduler 
which takes in a starting node (seen as the plan) and runs this starting node.
The schedule node is responsible for queueing other nodes which are ready to run. 
The schedule node checks which nodes can be run after it executed its internal component,
all nodes to the queue are given to the scheduler via the notify function 
given to the scheduled node on execution.

The scheduler makes the following assumptions:
- The given plan is correct
- There is a single input node (named starting node)
- The input node has exactly one input
- All nodes to run are accessible via the starting node
- Output handling to objects outside the plan or to the caller of the
scheduler is done inside the output components

## scheduling.plan

The plan is a graph with uni-directional connections between nodes.
It contains no cycles.
The plan can currently only be written in Python via schedule node definitions.
Plan creation might be extended using a parser to allow for a more
readable and adaptable format.

The plan is written using a bottom-up approach.
This is necessary since Python needs the node definition of `out_nodes` to 
happen before the current node is defined.
This also prevents cycles since a node can't output to itself or a node 
which has itself in their respective `out_nodes` list.

A schedule node is defined as follows:
```python
from scheduling.node.schedule_node import INode, ScheduleNode
from scheduling.component.example_components.example_component import ExampleComponent

number_of_inputs: int
out_node: INode
arg_nr: int
example_schedule_node = ScheduleNode(number_of_inputs, [(out_node, arg_nr)], ExampleComponent())
``` 
It is important to note that the `arg_nr` must correspond to the index array 
containing the expected input object, and the `number_of_inputs` is the length 
of the arguments list, which must be complete before node execution.

The last defined node in the Python plan is the input node of the schedule (or starting node). 
This node must have exactly one input.
```python
from scheduling.node.schedule_node import INode, ScheduleNode
from scheduling.component.example_components.input_component import InputComponent

out_node: INode
arg_nr: int
example_schedule_node = ScheduleNode(1, [(out_node, arg_nr)], InputComponent())
```

The first defined node in the Python plan is the last output node.
The `out_nodes` list (contains nodes to output its results to) can be left empty, 
like any other output nodes without `out_nodes`.
```python
from scheduling.node.schedule_node import ScheduleNode
from scheduling.component.example_components.output_component import OutputComponent

number_of_inputs: int
example_schedule_node = ScheduleNode(number_of_inputs, [], OutputComponent())
```

An example plan composed using the [example_components](component/example_components) 
can be found in [example_plan.py](plan/example_plan.py).

## scheduling.node

The scheduler node [schedule_node.py](node/schedule_node.py) is responsible for running 
the component once it is called by the scheduler 
(can only be called by the scheduler once all needed arguments have been collected) 
Furthermore, returning the output of the component to all out_nodes which need that output.

The schedule node overrides all functions of the interface node [INode](node/schedule_node.py).
Why the interface is necessary is explained in the Interface Node section.

The ScheduleNode is initialized using the following parameters:
- `input_count`: number of arguments needed to execute component
- `out_nodes`: list of nodes to which the current node assigns the output of the component 
(nodes that have the current node as input)
- `component`: the component to run once all necessary arguments have been collected

### scheduling.node.i_node

The interface node [INode](node/inode.py) is a superclass used as an interface.
It contains four functions that must be implemented by any subclass.
The implementation of a function is ensured by having the default implementation
raise a not implemented error.
The interface is used by the scheduler to assign the initial input object, 
check if a node is executable, 
reset the starting node for the next iteration, 
and execute the node.
The interface is also used by the `ScheduleNode` to assign arguments to `out_nodes`, 
check if a node is executable, 
and reset `out_nodes` for the next iteration.

The specification of the four interface functions:
- `reset()`: reset inputs of node for next iteration
- `executable()`: checks if self is executable (has all necessary arguments to run)
- `execute(notify: Callable[[list[Any]], None])`: execute the component belonging 
to the node with all provided argument, 
give the output of the component to all `out_nodes` 
and notify the scheduler of all nodes that are now ready to run.
- `assign(arg: object, arg_nr: int)`: store argument object at given index (`arg_nr`)

## scheduling.component

A component is a class being executed in a [ScheduleNode](node/schedule_node.py).
The component was designed to impose as few restrictions as possible
while simultaneously giving the scheduler the freedom it needs to properly operate.

Each component has three requirements:
- It must be written as a subclass of [IComponent](component/component_interface.py)
- It must override the function [execute_component()](component/base_component.py), 
returning the function used to run the component with any input defined in the function

Any given component is used for every given iteration.
It thus must be in a ready state after performing its work.
The class itself is responsible for possible resets to be performed,
storing data for the next iteration,
outputting to objects outside of the scheduler. 
(further explained in the Output Component section), etc.

The base component [BaseComponent](component/base_component.py) contains the basic form
any component should have.
Example components can be found in [component/example_components](component/example_components).

### scheduling.component.i_component

The component interface [component_interface.py](component/component_interface.py) 
replicates an interface in Python.
It defines the function `execute_component()` with a body only containing a 
`raise NotImplementedError` error, thus requiring any subclass of 
`IComponent` to override this function.
Any implementation of this function should return a non-applied function.

### scheduling.component.base_component

The base component [base_component.py](component/base_component.py) contains 
the minimum each component class should contain.
It overrides [execute_component()](component/base_component.py), 
returning a non-applied function that performs all the work.
The work function can contain any number of inputs (0 or more) as long as the number of inputs 
corresponds to the number of inputs given to [ScheduleNode](node/schedule_node.py).

### Input component

The input component [input_component.py](component/example_components/input_component.py) 
is slightly different.
It has the added restriction of containing exactly 1 input in the work function.
This one input can be `None` if no input is required but must be an object
containing all necessary information otherwise.

### Output component

The output component [output_component.py](component/example_components/output_component.py) 
or [intermediary_output_component.py](component/example_components/intermediary_output_component.py)
has no extra restrictions.
The only thing that needs to be mentioned is that any output component is responsible for
sending output to objects outside of the scheduler flow.

How this is done can depend on the use case. Below a few examples:
- A listener on the component watching its state
- A function to which output must be passed after completion of an iteration
- A direct call to the API used to pass data between 
the camera processor and processor orchestrator

It is expected that a node without `out_nodes` contains an output component.
Furthermore, any component can be an output component, and it already counts as
one if it emits output outside of the scheduler flow.
