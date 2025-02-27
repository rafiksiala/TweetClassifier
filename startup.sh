#!/bin/bash

# Lancer FastAPI en arrière-plan
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 127.0.0.1:8000 &

# Lancer Streamlit en arrière-plan
streamlit run app.py --server.port 8501 --server.address 127.0.0.1 &

# Démarrer NGINX
nginx -c nginx.conf
