#!/bin/bash

# Automatically get the username of the current user
USER_NAME=$(whoami)

# Set the app name here (e.g., "myapp" or "pro")
APP_NAME="pro"  # Change this variable to your app name, e.g., "myapp" or "pro"

# Define the local path to your repo (already pulled)
GITHUB_REPO_PATH="/home/$USER_NAME/apps/$APP_NAME"  # Adjust this to match your repo path
echo "Using GitHub repo path: $GITHUB_REPO_PATH"

# Define paths for the necessary files
GUNICORN_SERVICE_FILE="${GITHUB_REPO_PATH}/deploy/gunicorn/${APP_NAME}.service"
GUNICORN_SOCKET_FILE="${GITHUB_REPO_PATH}/deploy/gunicorn/${APP_NAME}.socket"
NGINX_CONFIG_FILE="${GITHUB_REPO_PATH}/deploy/nginx/${APP_NAME}"
ENV_FILE="${GITHUB_REPO_PATH}/deploy/environment/.env"

# Ensure the repo path exists
if [ ! -d "$GITHUB_REPO_PATH" ]; then
  echo "Error: Repository path $GITHUB_REPO_PATH does not exist. Exiting."
  exit 1
fi

# Copy Gunicorn service and socket files to the server
echo "Copying Gunicorn service and socket files..."
sudo cp $GUNICORN_SERVICE_FILE /etc/systemd/system/${APP_NAME}.service
sudo cp $GUNICORN_SOCKET_FILE /etc/systemd/system/${APP_NAME}.socket

# Enable and start Gunicorn services
echo "Enabling and starting Gunicorn service..."
sudo systemctl daemon-reload
sudo systemctl enable ${APP_NAME}.service
sudo systemctl enable ${APP_NAME}.socket
sudo systemctl start ${APP_NAME}.service

# Copy Nginx configuration file to the server
echo "Copying Nginx configuration file..."
sudo cp $NGINX_CONFIG_FILE /etc/nginx/sites-available/${APP_NAME}

# Create symlink for Nginx configuration
echo "Creating symlink for Nginx configuration..."
sudo ln -s /etc/nginx/sites-available/${APP_NAME} /etc/nginx/sites-enabled/${APP_NAME}

# Test Nginx configuration
echo "Testing Nginx configuration..."
sudo nginx -t

# Restart Nginx to apply the changes
echo "Restarting Nginx..."
sudo systemctl restart nginx

# Copy .env file to the server
echo "Copying .env file..."
cp $ENV_FILE /home/$USER_NAME/apps/${APP_NAME}/.env  # Use the local user to copy the .env file

# Final check: Ensure services are running
echo "Checking Gunicorn and Nginx status..."
sudo systemctl status ${APP_NAME}.service
sudo systemctl status nginx

echo "Deployment complete!"
