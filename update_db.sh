#!/bin/bash

echo "Setup up migrations..."
python3 movie_explorer/manage.py makemigrations &> /dev/null 2>&1
python3 movie_explorer/manage.py migrate