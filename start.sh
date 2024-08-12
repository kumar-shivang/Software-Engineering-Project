#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
  # Create a virtual environment
  python3 -m venv ./backend/venv
fi


# Activate the virtual environment
source ./backend/venv/bin/activate

cd backend/

# Install required Python packages
pip install -r requirements.txt

# Navigate back to the root of the project
cd ../frontend

# Install npm dependencies for the React app
yarn 

# Run both the React and Flask servers concurrently
npx concurrently "yarn start" "cd ../backend && flask run"
