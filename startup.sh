#!/bin/bash

# Lancer FastAPI avec Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 &

# Lancer Streamlit sur un autre port (ex: 8501)
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
