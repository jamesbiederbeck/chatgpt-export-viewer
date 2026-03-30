FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    jq \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# chats/ directory will be provided via volume mount at runtime
RUN mkdir -p chats && chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
