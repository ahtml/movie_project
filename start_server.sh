#!/bin/bash

echo "Migrate Database..."
./update_db.sh

echo "Run Server..."
python3 movie_explorer/manage.py runserver

echo "DONE"