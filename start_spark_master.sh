#!/bin/bash

# Step 1: Install the python3-venv package to enable venv creation
echo "Installing python3-venv..."
apt-get update && apt-get install -y python3.10-venv

# Step 2: Set up POETRY_HOME
export POETRY_HOME=/opt/poetry

# Step 3: Create a Python virtual environment for Poetry installation
echo "Creating a Python virtual environment for Poetry..."
python3 -m venv $POETRY_HOME

# Step 4: Install Poetry in the virtual environment
echo "Installing Poetry version..."
$POETRY_HOME/bin/pip install poetry==1.8.4

# Step 5: Verify Poetry installation
echo "Verifying Poetry installation..."
$POETRY_HOME/bin/poetry --version

# Step 6: Add Poetry to PATH for easier use
export PATH="$POETRY_HOME/bin:$PATH"

# Step 7: Install project dependencies using Poetry
echo "Installing project dependencies with Poetry..."
poetry install --no-root

tail -f /dev/null


# Step 8: Optional: Wait for all background tasks to finish
# This step isn't needed unless you're running background processes.
wait
