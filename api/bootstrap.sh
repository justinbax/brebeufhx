#!/bin/sh
export FLASK_APP=api/main.py
pipenv run flask --debug run -h 0.0.0.0 -p 3001


# You can also run pipenv run flask --app ./api/main.py --debug run -h 0.0.0.0 -p 3001