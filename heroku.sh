#!/bin/bash
python worker.py &
gunicorn app:app