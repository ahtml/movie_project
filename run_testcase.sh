#!/bin/bash

echo "Clear Database..."
./clear_db.sh

echo "ReSetup Database..."
./setup_db.sh

echo "Run Test..."
python3 movie_explorer/movie_rating/browser_tests.py

echo "DONE"

