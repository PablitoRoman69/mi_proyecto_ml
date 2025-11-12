#!/bin/bash
cd /api/
pip install --upgrade pip
pip install -r requirements.txt
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.api:app
uvicorn api.api:app --reload