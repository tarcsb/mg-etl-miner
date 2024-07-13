# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY setup.py /app/

# Install dependencies
RUN pip install --upgrade pip &&     pip install .

# Copy the project files
COPY . /app

# Expose the port for the application
EXPOSE 8000

# Define the command to run the application
CMD ["mg_miner", "--root_dir", "/data", "--output_dir", "/output", "--serve", "--theme", "light"]
