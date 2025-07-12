FROM python:3.12-alpine

WORKDIR /code

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    build-base

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


ENTRYPOINT ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port 8000"]
