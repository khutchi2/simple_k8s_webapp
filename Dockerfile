# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/text-app-code.py .

COPY app/templates/ templates/

EXPOSE 8080

CMD ["python", "text-app-code.py"]
