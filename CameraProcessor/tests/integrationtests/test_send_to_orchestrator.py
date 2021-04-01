# Talks to orchestrator

# Sends all possible API calls to orchestrator
# Asserts that no message is sent back to current processor

url = 'ws://processor-orchestrator-test-service/processor'
url = 'ws://localhost:80/processor'


websocket_test = WebsocketClient(url)