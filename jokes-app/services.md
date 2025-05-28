# Content Service

To run the Content Service with Dapr:

```sh
dapr run --app-id content-service --app-port 8001 -- uvicorn jokes-app.content_service:app --host 0.0.0.0 --port 8001
```

The service will be available at:

http://localhost:8001/jokes

# Rating Service

To run the Rating Service with Dapr:

```sh
dapr run --app-id rating-service --app-port 8002 -- uvicorn jokes-app.rating_service:app --host 0.0.0.0 --port 8002
```

The service will be available at:

- POST http://localhost:8002/rate/{joke_id} (with JSON body: {"rating": <int>})
- GET  http://localhost:8002/rating/{joke_id}

# Ranking Service

To run the Ranking Service with Dapr:

```sh
dapr run --app-id ranking-service --app-port 8003 -- uvicorn jokes-app.ranking_service:app --host 0.0.0.0 --port 8003
```

The service will be available at:

http://localhost:8003/ranking

# Stats Service

To run the Stats Service with Dapr:

```sh
dapr run --app-id stats-service --app-port 8004 -- uvicorn jokes-app.stats_service:app --host 0.0.0.0 --port 8004
```

The service will be available at:

- POST http://localhost:8004/stats/rating
- POST http://localhost:8004/stats/view
- GET  http://localhost:8004/stats

# Content Delivery Service

To run the Content Delivery Service with Dapr:

```sh
dapr run --app-id content-delivery-service --app-port 8005 -- uvicorn jokes-app.content_delivery_service:app --host 0.0.0.0 --port 8005
```

The service will be available at:

- POST http://localhost:8005/upload (multipart/form-data, field: file)
- GET  http://localhost:8005/media/{filename}

# Frontend Gateway

To run the Frontend Gateway with Dapr:

```sh
dapr run --app-id frontend-gateway --app-port 8006 -- uvicorn jokes-app.frontend_gateway:app --host 0.0.0.0 --port 8006
```

The service will be available at:

- GET http://localhost:8006/jokes/full
- GET http://localhost:8006/health
