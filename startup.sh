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

        # Redirection vers Streamlit
        location / {
            proxy_pass http://127.0.0.1:8001/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        }

        # Redirection vers FastAPI
        location /api/ {
            proxy_pass http://127.0.0.1:8002/;
            proxy_http_version 1.1;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        }
    }
}
EOF

# Démarrer NGINX
service nginx start

# Lancer FastAPI avec Gunicorn en arrière-plan
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 127.0.0.1:8002 &

# Lancer Streamlit en arrière-plan (ajout de `&` pour éviter le blocage)
streamlit run app.py --server.port 8001 --server.address 127.0.0.1 &
