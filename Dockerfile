FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_MODULE="content_service:app"
ENV APP_PORT=8001

EXPOSE $APP_PORT

CMD ["sh", "-c", "uvicorn $APP_MODULE --host 0.0.0.0 --port $APP_PORT"]
