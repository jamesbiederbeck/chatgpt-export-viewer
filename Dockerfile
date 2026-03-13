FROM python:3.11-slim

WORKDIR /app

COPY . .

# chats/ directory will be provided via volume mount at runtime
RUN mkdir -p chats

EXPOSE 8000

CMD ["python", "server.py"]
