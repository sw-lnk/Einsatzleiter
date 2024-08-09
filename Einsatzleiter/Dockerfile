# Use Python 3.11.9 image based on Linux Alpine
FROM python:3.11.9-alpine

# Set an environment variable to unbuffer Python output, aiding in logging and debugging
ENV PYTHONBUFFERED=1

# prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Define an environment variable for the web service's port, commonly used in cloud services
ENV PORT 8080

# Set the working directory within the container to /app for any subsequent commands
WORKDIR /usr/src/app
RUN mkdir staticfiles
RUN mkdir mediafiles

# Copy the entire current directory contents into the container at /app
COPY . /usr/src/app/

# Upgrade pip to ensure we have the latest version for installing dependencies
RUN pip install --upgrade pip

# Install dependencies from the requirements.txt file to ensure our Python environment is ready
RUN pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Set the command to run our web service using Gunicorn, binding it to 0.0.0.0 and the PORT environment variable
CMD gunicorn server.wsgi:application --bind 0.0.0.0:"${PORT}"

# Inform Docker that the container listens on the specified network port at runtime
EXPOSE ${PORT}

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
