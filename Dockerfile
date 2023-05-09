FROM python:3.11.3-alpine3.16

WORKDIR /app

COPY . .

CMD ["python", "main.py"]