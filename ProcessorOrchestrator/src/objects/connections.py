"""File which contains dicts with the currently open websocket connections.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

processors = dict()
"""Dictionary which matches processor id to the corresponding WebSocket

type: Dict[str, ProcessorSocket]
"""

clients = dict()
"""Dictionary, which matches client id to the corresponding WebSocket

type: Dict[str, ClientSocket]
"""
