import flask
from dapr.clients import DaprClient
import os

app = flask.Flask(__name__)

# Dapr publishes messages with Content-Type: application/json
# and dapr.io/app-id header for service invocation
# So we disable Flask's default JSON parsing for now to see raw input
app.config["JSON_AS_ASCII"] = False
app.config["DEBUG"] = True


@app.route('/hello', methods=['GET'])
def hello_world():
    print("Callee received a 'hello' request!")
    return flask.Response("Hello from Callee!", mimetype='text/plain')

if __name__ == '__main__':
    app_port = os.getenv('APP_PORT', '5001')
    app.run(port=app_port)