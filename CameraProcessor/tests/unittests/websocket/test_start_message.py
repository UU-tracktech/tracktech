"""Tests StartMessage.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from processor.websocket.start_message import StartMessage

# BASE64IMAGE = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABcAAAAYCAYAAAARfGZ1AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGfSURBVEhL7ZRbT8JAEIX9PUtLqwXbElPuAUwp97ZAAhoUWn0xxgRN0Bq0+rOPZaEXEPTB6IPh4aRpz+w3OzO7PYjFYvgt7eFbtYdv1R6+VX8DJ4RH5c6ErjGByddVTGZFyAzxfA7lWxPdJhf4USmXOq7eu1T2m4pcnOyGE/YYtZkOs7aEfQdnBQ6CyEPIF3Dmw3lCqLkJF9oarIcCJNb31+GEMBDNGibTfBBDv8tZDH14pxpfBYdwwkloOTo61XCXm3BGyWEwb0BNh22kcVH4eCytFi/hlmvAejVgP5WQ8nodLIrACZtAdapj0EuAWVUexEXh9vUJDfDhXT2BZDaHvtuClgl35cMXiWny5zKUSPIg7is4bQthkbE7GHtePJjJEt7vJZFU0jDmHbRPly3dCd9siz9QJp3HuVtHWV6H07Z4CZNmHdZ9OHBfRMpiEAxU/TxQH1a8MTAaiavK1gdKOBHNRwPd1vrRJFwKuutVpQm7j+JCbKmMixcV+cT2S3TY8C6ZU4HCh7tfVCU2TzF0jP/y4zqSBehOnz5//h7DB8/YdjJhkrsuAAAAAElFTkSuQmCC "


# class TestStartCommand:
#     def test_from_message_to_message(self):
#         """beep boop."""
#         message = {
#             "objectId": 1,
#             "image": BASE64IMAGE
#         }
#         startcommand = StartMessage.from_message(message)
#         json_message = startcommand.to_message()
#         assert json_message["image"] == message["image"]
