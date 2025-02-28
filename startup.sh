#!/bin/bash

# Lancer FastAPI avec Gunicorn sur le port 8000
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 &

# Lancer Streamlit sur un autre port (8501)
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
