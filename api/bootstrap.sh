#!/bin/sh
export FLASK_APP=api/main.py
pipenv run flask --debug run -h 0.0.0.0 -p 3000
