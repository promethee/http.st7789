#!/bin/sh
export FLASK_APP=main
export FLASK_ENV=development
python3 -m flask run --host=0.0.0.0
