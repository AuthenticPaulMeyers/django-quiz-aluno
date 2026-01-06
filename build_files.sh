#!/bin/bash
# build_files.sh
echo "Building the project..."
python3.14 -m pip install -r requirements.txt
echo "Make Migration..."
python3.14 manage.py makemigrations --noinput
python3.14 manage.py migrate --noinput
echo "Collect Static..."
python3.14 manage.py collectstatic --noinput --clear
