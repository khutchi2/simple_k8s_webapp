# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Make port 5000 available
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]