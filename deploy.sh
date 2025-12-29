#!/bin/bash
# deploy.sh

# Stop script on error
set -e

# --- CONFIGURATION ---
DOMAIN="ktlab.store"
IP="194.67.124.149"
REPO="https://github.com/Beiseek/dron.git"
PROJECT_DIR="/var/www/dron-site"
# ---------------------

echo "=========================================="
echo "STARTING DEPLOYMENT TO $IP ($DOMAIN)"
echo "=========================================="

# 1. Update System
echo "[1/9] Updating system packages..."
apt-get update -qq && apt-get upgrade -y -qq

# 2. Install Dependencies
echo "[2/9] Installing system dependencies..."
apt-get install -y -qq python3-venv python3-dev python3-pip nginx git certbot python3-certbot-nginx sqlite3 libsqlite3-dev

# 3. Clone/Update Repository
echo "[3/9] Setting up project files..."
if [ -d "$PROJECT_DIR" ]; then
    echo "Directory exists. Removing old version to ensure clean slate..."
    rm -rf "$PROJECT_DIR"
fi
echo "Cloning repository..."
git clone "$REPO" "$PROJECT_DIR"
cd "$PROJECT_DIR"

# 4. Setup Virtual Environment
echo "[4/9] Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 5. Django Configuration
echo "[5/9] Configuring Django..."
# Run migrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput

# Create superuser (admin/admin) if not exists
echo "Creating default superuser..."
cat <<EOF | python3 manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser "admin" created.')
else:
    print('Superuser "admin" already exists.')
EOF

# 6. Setup Gunicorn
echo "[6/9] Configuring Gunicorn..."
cat > /etc/systemd/system/gunicorn.service <<EOF
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --access-logfile - --workers 3 --bind 127.0.0.1:8000 dron_site.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable gunicorn
systemctl restart gunicorn

# 7. Setup Nginx
echo "[7/9] Configuring Nginx..."
cat > /etc/nginx/sites-available/dron <<EOF
server {
    listen 80;
    server_name $DOMAIN $IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
    }

    location /media/ {
        alias $PROJECT_DIR/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/dron /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Set Permissions
mkdir -p $PROJECT_DIR/media
chown -R www-data:www-data $PROJECT_DIR/media
chmod -R 775 $PROJECT_DIR/media
chown -R www-data:www-data $PROJECT_DIR/staticfiles
chmod -R 755 $PROJECT_DIR/staticfiles

# Check and restart Nginx
nginx -t
systemctl restart nginx

# 8. SSL Certificate
echo "[8/9] Setting up SSL with Let's Encrypt..."
# Using --non-interactive mode
certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m admin@ktlab.store --redirect

# 9. Final Check
echo "=========================================="
echo "DEPLOYMENT COMPLETE!"
echo "Website: https://$DOMAIN"
echo "Admin Panel: https://$DOMAIN/admin"
echo "Login: admin"
echo "Password: admin"
echo "=========================================="
