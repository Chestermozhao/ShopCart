#!/bin/bash

exec gunicorn --graceful-timeout 25 --max-requests 100000 --max-requests-jitter 2000 -w 2 -t 25 -b 0.0.0.0:8000 backend.asgi

