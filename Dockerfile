# syntax=docker/dockerfile:1

FROM python:3.9-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy over the API file
COPY api.py .

# Container opens the API on this port
EXPOSE 8100

# Start application
CMD [ "python3", "api.py" ]
