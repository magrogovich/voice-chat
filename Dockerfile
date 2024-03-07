# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the local requirements.txt file to the container at /app
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local project files to the container at /app
COPY . /app/

# Expose the port that your server is running on
EXPOSE 3000

# Command to run your application
CMD ["python", "server.py"]
