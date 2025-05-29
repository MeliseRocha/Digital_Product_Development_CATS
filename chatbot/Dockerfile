FROM rasa/rasa:latest

# Switch to root to install packages
USER root

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make sure the rasa user can write to the directory
RUN chown -R 1001:1001 /app

# Switch back to the rasa user for security
USER 1001

# Default command (overridden in docker-compose)
CMD ["rasa", "--help"]
