# Use an official lightweight Python image as a base
FROM python:3.11-slim

# Set a working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's caching mechanism.
# This layer will only be rebuilt if requirements.txt changes.
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that Gunicorn will run on
EXPOSE 8000

# The command to run your application using a production-ready server
# 0.0.0.0 is crucial to allow connections from outside the container
CMD ["gunicorn", "--workers=2", "--bind", "0.0.0.0:8000", "app:app"]