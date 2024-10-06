# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file first
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application source code to the container
COPY ./src ./src

# Expose the port the app runs on
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["uvicorn", "src.main:backend_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
