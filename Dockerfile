FROM python:3.11-slim

WORKDIR /app

# Copy the requirements file and install dependencies FIRST
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# The build.sh script will have already run and created all our files.
# This single command copies the entire project, including the downloaded models.
COPY . .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]