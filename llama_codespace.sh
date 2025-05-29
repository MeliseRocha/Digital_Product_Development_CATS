#!/bin/bash

# Step 1: Install Ollama
echo "Downloading and installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Step 2: Start Ollama service
echo "Starting Ollama service..."
nohup ollama serve > ollama.log 2>&1 &

# Step 3: Check if Ollama service is running
echo "Waiting for Ollama to start..."
sleep 5

# Step 4: Verify if Ollama is running
if curl -s http://127.0.0.1:11434/ > /dev/null; then
    echo "Ollama service is up and running!"
else
    echo "Failed to start Ollama. Please check the logs at ollama.log."
fi

# Step 5: Optionally run a model (e.g., phi) to confirm it's working
echo "Running model 'phi'..."
ollama run phi
