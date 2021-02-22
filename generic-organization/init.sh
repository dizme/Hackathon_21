#!/bin/bash
set -e

python3 manage.py makemigrations && python3 manage.py migrate
echo "DBINIT OK"
echo "FINISHED"