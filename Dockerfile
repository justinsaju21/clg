
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Create a non-root user and switch to it (Render Best Practice)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Run gunicorn
# CMD is strictly optional for Render if you set the 'Start Command' in the dashboard,
# but good to have as default.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
