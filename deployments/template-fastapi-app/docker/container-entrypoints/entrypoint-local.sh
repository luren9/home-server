#!/bin/sh
echo "Running local development container (Not intended for production use)"

exec uvicorn app.main:app --host 0.0.0.0 --port 5000