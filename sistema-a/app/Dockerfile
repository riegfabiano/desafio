# Use an official Python runtime as a parent image
FROM python:3.6.4-alpine3.7

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD ./app /app

# Copy the requirements into the container at /etc
COPY ./requirements.txt /etc

# Install any needed packages specified in requirements.txt
RUN pip install -r /etc/requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 5001

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]