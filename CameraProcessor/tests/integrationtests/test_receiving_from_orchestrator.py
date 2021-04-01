# Listens to what orchestrator sends through

# Expects to hear messages from orchestrator via other processor
# Gets to hear feature map API calls from orchestrator when other processor sends them

url = 'ws://processor-orchestrator-test-service/processor'
url = 'ws://localhost:80/processor'
websocket_test = WebsocketClient(url)