# Use the official Python 3.10 image as the base
FROM python:3.10

# Set the working directory in the container
WORKDIR /messaging_app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .


# Expose the port the Django app runs on (default 8000)
EXPOSE 8000

# Define the command to run the application when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

