# Use the Python 3.10-slim image as the base image
FROM python:3.10-slim

# Install required packages (curl)
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Download and install k6 version 0.46 for x64
RUN curl -OL https://github.com/loadimpact/k6/releases/download/v0.46.0/k6-v0.46.0-linux-amd64 \
    && chmod +x k6-v0.46.0-linux-amd64 \
    && mv k6-v0.46.0-linux-amd64 /usr/local/bin/k6 \
    && rm -f k6-v0.46.0-linux-amd64

# Create a directory for your app and navigate to it
WORKDIR /app

# Copy your Streamlit app code to the working directory
COPY . /app/

# Install Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Streamlit will run on (default is 8501)
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Specify the command to run when the container starts
ENTRYPOINT  ["streamlit", "run", "app.py", "--server.port=8501"]

