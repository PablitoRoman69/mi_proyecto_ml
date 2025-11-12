#!/bin/bash
cd /home/site/wwwroot
pip install --upgrade pip
pip install -r requirements.txt
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.api:app