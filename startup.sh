#!/bin/bash

# Lancer FastAPI avec Gunicorn sur le port 8000 (accessible publiquement)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
