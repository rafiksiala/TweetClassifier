#!/bin/bash

# Lancer Streamlit en premier sur le port principal 8000
streamlit run app.py --server.port 8000 --server.address 0.0.0.0 &

# Lancer FastAPI sur un autre port (ex: 8501)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8501
