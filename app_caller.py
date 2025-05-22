import flask
from dapr.clients import DaprClient
import os
import time

app = flask.Flask(__name__)

@app.route('/invoke', methods=['GET'])
def invoke_callee():
    callee_app_id = "callee"
    method_name = "hello"

    with DaprClient() as client:
        # Invoke a method on the callee service
        print(f"Invoking {method_name} on {callee_app_id}...")
        response = client.invoke_method(
            app_id=callee_app_id,
            method_name=method_name,
            http_verb="GET",
            data=""
        )
        print(f"Response from callee: {response.text()}")
        return flask.Response(f"Caller invoked callee: {response.text()}", mimetype='text/plain')

if __name__ == '__main__':
    app_port = os.getenv('APP_PORT', '5000')
    app.run(port=app_port)