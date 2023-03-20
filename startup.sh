#!/bin/sh
source venv/bin/activate
gunicorn -b :5000 --access-logfile - --error-logfile - app.wsgi:app