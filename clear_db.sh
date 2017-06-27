#!/bin/bash

echo "Removing db.sqlite3..."
rm movie_explorer/db.sqlite3

echo "Removing migrations python cache files..."
rm -r movie_explorer/movie_rating/migrations/__pycache__

# Delete all files in migrations/ except __init__.py
find movie_explorer/movie_rating/migrations/*.py -not -name __init__.py | xargs rm

echo "DONE"