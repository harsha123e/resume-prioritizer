#!/bin/bash
set -e

# Source virtual environment activation script (if applicable)
# source venv/bin/activate  # Example for venv activation

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --no-input
