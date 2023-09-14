# Use a arm v8 with ubuntu as the base.
FROM arm32v7/python:3.7.8

# Set the working directory in the container
WORKDIR /home/pi/Exolith_Lab-1.2.3

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Ensure pip is up to date
RUN pip install --no-cache-dir --upgrade pip setuptools

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the container
COPY . .

# Set the command to run your application
CMD [ "python", "./Mark_IV/Sintering/solarAlignment.py" ]
