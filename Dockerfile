FROM python:3.11-slim

WORKDIR /app

# The build.sh script will have already run and created all our files.
# This single command copies the entire project, including the downloaded models.
COPY . .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.-0.0.0:5000", "app:app"]