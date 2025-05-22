# How to launch
### Initial commands:
`pip install dapr`

`pip install flask`

`dapr init`

### Zipkin (does not work yet)
Restart and launch:
```bash
docker stop $(docker ps -aq --filter ancestor=openzipkin/zipkin)
docker rm $(docker ps -aq --filter ancestor=openzipkin/zipkin)
docker run -d -p 9411:9411 -p 4317:4317 openzipkin/zipkin
```
Usage: http://localhost:9411

### Services
`dapr run --app-id callee --app-port 5001 --dapr-http-port 3501 --config ./config.yaml python app_callee.py`

`dapr run --app-id caller --app-port 5000 --dapr-http-port 3500 --config ./config.yaml python app_caller.py`

### Test if works
`curl http://localhost:5000/invoke`

"Caller invoked callee: Hello from Callee!" is a correct answer.