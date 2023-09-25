# Use the Python 3.10-slim image as the base image
FROM python:3.10-slim

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

