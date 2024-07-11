#!/bin/bash
set -e

echo "Installing dependencies..."
python3.12 -m pip install --upgrade pip
pip install -r requirements.txt

echo "Running migrations..."
python3.12 manage.py migrate

echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput
