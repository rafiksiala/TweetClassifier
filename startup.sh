#!/bin/bash

# Lancer FastAPI avec Gunicorn en arrière-plan sur le port 8001
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8001 &

# Lancer Streamlit sur le port 8000 (port public)
streamlit run app.py --server.port 8000 --server.address 0.0.0.0
