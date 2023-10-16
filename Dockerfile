# FROM python:3.11

# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# COPY requirements.txt /app/

# RUN pip install -r requirements.txt

# COPY event /app/

# EXPOSE 8000

# CMD [ "python","manage.py","runserver","127.0.0.1:8000"]

# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY event /app/

# Expose port 8000
EXPOSE 8000

# Start the application
CMD ["python", "manage.py", "runserver"]
