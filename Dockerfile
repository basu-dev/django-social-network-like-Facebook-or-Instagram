# Use the official Python image as a base
FROM python:3.8

# Set environment variables to prevent Python from writing pyc files and buffering stdout
ENV PYTHONUNBUFFERED=1

# Install system dependencies including libpq-dev for PostgreSQL
RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Create and set the working directory for the Django application
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django application code into the container
COPY . /app/

RUN python manage.py makemigrations
RUN python manage.py migrate 

# Expose the port the app will run on
EXPOSE 8000

# Set the default command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
