# ./chatbot/actions/Dockerfile
FROM rasa/rasa-sdk:latest

# Switch to root to install packages
USER root

# Copy requirements.txt first
COPY requirements.txt .

# Install psycopg2-binary and any other dependencies
RUN pip install -r requirements.txt

# Switch back to the default user
USER 1001