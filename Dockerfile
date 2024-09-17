# Use the Python 3.10-slim image as the base image
#FROM python:3.10-slim

#FROM alpine:latest
FROM ubuntu:latest

# Create a directory for your app and navigate to it
WORKDIR /app

# Copy your Streamlit app code to the working directory
COPY . /app/

# Install Python packages from requirements.txt

RUN apt-get -y update && apt-get install -y apt-transport-https
RUN apt-get install -y python3-pip
#RUN pip3 install streamlit --break-system-packages
#RUN pip3 install --upgrade pip
#RUN pip3 install streamlit
#RUN apk add --update --no-cache python3 py-pip
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

RUN apt-get install -y ca-certificates
RUN apt-get install -y gnupg dirmngr
RUN gpg -k
RUN gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
RUN echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | tee /etc/apt/sources.list.d/k6.list
RUN apt-get update
RUN apt-get install k6

#RUN pip install streamlit

# Expose the port that Streamlit will run on (default is 8501)
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Specify the command to run when the container starts
ENTRYPOINT  ["streamlit", "run", "app.py", "--server.port=8501"]
