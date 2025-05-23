**Czego potrzebujesz:**

- Dapr CLI ()
- Docker-compose
- python3

### Uruchomienie serwera

Zainstaluj package do pythona

```sh
pip install -r requirements.txt
```

A następnie przy pomocy dapr uruchom serwer fastAPI

```sh
dapr run --app-id fastapi-app --app-port 8000 -- uvicorn app:app --host 0.0.0.0 --port 8000
```

Aplikacja powinna być dostępna pod adresem http://localhost:9680/v1.0/invoke/fastapi-app/method/hello (Może uruchomić się na innym porcie)

```sh
curl http://localhost:9680/v1.0/invoke/fastapi-app/method/hello
```
```json
{"message":"Hello, FastAPI!"}
```

### Uruchomienie otel-collector, prometheus i grafana

Przejdź do folderu `/metrics` i uruchom `docker-compose up`

```sh
cd ./metrics
docker-compose up
```

Pod adresem http://localhost:3000 powinna być dostępna grafana - domyślne credentiale to

```
user: admin
password: admin
```

Dodaj nowe źródło danych z `Prometheus` i podaj w nim adres http://prometheus:9090
