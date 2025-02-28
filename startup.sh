#!/bin/bash

# Vérifier si NGINX est déjà installé (évite les redémarrages)
if ! command -v nginx &> /dev/null
then
    echo "Installation de NGINX..."
    apt-get update && apt-get install -y nginx
fi

# Copier la configuration de NGINX
cat > /etc/nginx/nginx.conf <<EOF
worker_processes 1;

events {
    worker_connections 1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    keepalive_timeout 65;

    server {
        listen 8000;

        location / {
            proxy_pass http://127.0.0.1:8501/;  # Redirige vers Streamlit
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        }

        location /api/ {
            proxy_pass http://127.0.0.1:8001/;  # Redirige vers FastAPI
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        }
    }
}
EOF

# Démarrer NGINX (sans daemon off, car Azure gère les processus)
service nginx start

# Lancer FastAPI avec Gunicorn en arrière-plan
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 127.0.0.1:8001 &

# Lancer Streamlit en arrière-plan
streamlit run app.py --server.port 8501 --server.address 127.0.0.1
