#!/bin/sh
echo "Running production grade container (intended for kubernetes/production use)"

exec uvicorn app.main:app --host 0.0.0.0 --port 5000