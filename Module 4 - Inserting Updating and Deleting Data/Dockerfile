# Use official Python image
FROM python:3.13.2-alpine3.21

# Set working directory
WORKDIR /app

# Install system dependencies required for psycopg2
RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev

# Copy project files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000