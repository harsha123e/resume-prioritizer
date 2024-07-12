#!/bin/bash

# Create and activate a virtual environment
python3.9 -m venv venv
source venv/bin/activate

python3.9 -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput
