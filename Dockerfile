# Use an official Python image as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the Python script
COPY producthunt_scraper.py .

# Run the Python script
CMD ["python", "producthunt_scraper.py"]