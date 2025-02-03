# Flask App Deployment with Nginx and Gunicorn

## Overview
This guide outlines the setup and deployment of a Flask application using Nginx and Gunicorn on a Raspberry Pi.

## Project Structure
Ensure your Flask project is structured as follows:

```
/home/pi/apps/flask_app
├── app.py (Flask application)
├── templates/
├── static/
├── env/ (virtual environment)
├── requirements.txt
└── config/
```

## 1. Install Dependencies
```bash
sudo apt update && sudo apt install -y python3-pip python3-venv nginx
```

## 2. Set Up a Virtual Environment
```bash
cd /home/pi/apps/flask_app
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## 3. Gunicorn Configuration
Create a systemd service file at `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=Gunicorn daemon for Flask app
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=/home/pi/apps/flask_app
ExecStart=/home/pi/apps/flask_app/env/bin/gunicorn --workers 3 --bind unix:/home/pi/apps/flask_app/gunicorn.sock app:app

[Install]
WantedBy=multi-user.target
```

Enable and start Gunicorn:
```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## 4. Nginx Configuration
Create an Nginx configuration file at `/etc/nginx/sites-available/flask_app`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        root /home/pi/apps/flask_app;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/pi/apps/flask_app/gunicorn.sock;
    }
}
```

Enable the site and reload Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
```

## 5. File Permissions
```bash
sudo chown -R pi:www-data /home/pi/apps/flask_app
sudo chmod -R 755 /home/pi/apps/flask_app
```

## 6. Restart Services
```bash
sudo systemctl restart gunicorn
sudo systemctl reload nginx
```

## 7. Test the Setup
Visit `http://yourdomain.com` to confirm the application is running.

## 8. Additional Steps
- Update `requirements.txt`:
```bash
pip freeze > requirements.txt
```
- Restart the app after changes:
```bash
sudo systemctl restart gunicorn
```

Your Flask application should now be running with Nginx and Gunicorn.

