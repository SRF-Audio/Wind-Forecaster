# Use an official Python runtime as the parent image
FROM python:3.9-slim

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set an environment variable to ensure that Python doesn't try to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Set an environment variable to ensure that Python doesn't buffer its output
ENV PYTHONUNBUFFERED 1

# Install any necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /app/

# Command to run on container start
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

