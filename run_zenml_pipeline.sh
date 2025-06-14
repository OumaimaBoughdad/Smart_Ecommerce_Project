#!/bin/bash

# Install ZenML and dependencies
echo "Installing ZenML and dependencies..."
pip install -r requirements-zenml.txt

# Initialize ZenML if not already initialized
if [ ! -d ".zenml" ]; then
    echo "Initializing ZenML..."
    zenml init
fi

# Set up ZenML stack
echo "Setting up ZenML stack..."
python zenml_setup.py

# Run the pipeline
echo "Running product scoring pipeline..."
python zenml_pipeline.py

# Start ZenML dashboard
echo "Starting ZenML dashboard..."
zenml up

echo "Setup complete! Access the ZenML dashboard at http://127.0.0.1:8237"