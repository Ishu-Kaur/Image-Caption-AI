# Use an official lightweight Python image as a base
FROM python:3.11-slim

# Set a working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's caching mechanism.
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that Gunicorn will run on
EXPOSE 8000

# --- THIS IS THE CORRECTED LINE ---
# We change the number of workers from 2 to 1 to reduce memory usage.
CMD ["gunicorn", "--workers=1", "--bind", "0.0.0.0:8000", "app:app"]