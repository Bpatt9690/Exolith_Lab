# Use an official Python runtime as the base image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the container
COPY . .

# Copy the .env file to the container
COPY .env .

# Set the command to run your application
CMD [ "python", "../Mark_IV/Sintering/solarAlignment.py" ]
