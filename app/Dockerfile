FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py schema.sql ./
COPY templates/ ./templates/

# Create a non-root user to run the app
RUN useradd -m flaskuser
RUN mkdir -p /app/data && chown -R flaskuser:flaskuser /app

USER flaskuser

CMD ["python", "app.py"]
