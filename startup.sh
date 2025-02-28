#!/bin/bash

# Installer NGINX et Gunicorn (Azure Web App Linux ne garde pas les paquets après un redémarrage)
apt-get update && apt-get install -y nginx gunicorn

# Copier la configuration de NGINX (création du fichier de config)
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

# Démarrer NGINX
nginx &

# Lancer FastAPI avec Gunicorn en arrière-plan
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 127.0.0.1:8001 &

# Lancer Streamlit en arrière-plan
streamlit run app.py --server.port 8501 --server.address 127.0.0.1
