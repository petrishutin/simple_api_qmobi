#!/bin/bash
set -e
if [ "$ENV" = 'RUN' ]; then
  exec python main.py
elif [ "$ENV" = 'TEST' ]; then
  exec python -m unittest discover tests
fi