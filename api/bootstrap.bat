@echo off
pipenv run flask --app .\api\main.py --debug run -h 0.0.0.0 -p 3000