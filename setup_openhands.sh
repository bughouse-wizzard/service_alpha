#!/bin/bash

# OpenHands Setup Script
# Custom deployment with network fixes

set -e

echo "=== OpenHands Setup Script ==="
echo "Starting installation..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
    sudo usermod -aG docker $USER
    echo "Docker installed. Please log out and log back in for group changes to take effect."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "Docker is not running. Starting Docker..."
    sudo systemctl start docker
    sudo systemctl enable docker
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p ~/.openhands
mkdir -p workspace

# Set permissions
echo "Setting permissions..."
sudo chmod 666 /var/run/docker.sock || true

# Build custom OpenHands image
echo "Building OpenHands custom image..."
docker build -t openhands:custom-1.2.1 -f ./containers/app/Dockerfile .

# Stop any existing containers
echo "Stopping any existing OpenHands containers..."
docker compose -f docker-compose-custom.yml down || true

# Start OpenHands
echo "Starting OpenHands..."
docker compose -f docker-compose-custom.yml up -d

# Wait for startup
echo "Waiting for OpenHands to start..."
sleep 10

# Check if OpenHands is running
if curl -s http://localhost:3000/api/health > /dev/null; then
    echo "✅ OpenHands is running successfully!"
    IP=$(hostname -I | awk '{print $1}')
    echo "Access at: http://$IP:3000"
    echo "or http://localhost:3000"
else
    echo "⚠️  OpenHands might be starting up. Checking logs..."
    docker compose -f docker-compose-custom.yml logs --tail=20 openhands
fi

# Create systemd service for auto-start
echo "Creating systemd service..."
sudo tee /etc/systemd/system/openhands.service > /dev/null << 'SYSEOF'
[Unit]
Description=OpenHands AI Development Platform
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/av/openhands
ExecStart=/usr/bin/docker compose -f /home/av/openhands/docker-compose-custom.yml up -d
ExecStop=/usr/bin/docker compose -f /home/av/openhands/docker-compose-custom.yml down
User=av
Group=docker

[Install]
WantedBy=multi-user.target
SYSEOF

# Create startup script
echo "Creating startup script..."
sudo tee /usr/local/bin/start-openhands > /dev/null << 'STARTEOF'
#!/bin/bash
cd /home/av/openhands
docker compose -f docker-compose-custom.yml up -d
STARTEOF

sudo chmod +x /usr/local/bin/start-openhands

# Enable and start service
echo "Enabling OpenHands service..."
sudo systemctl daemon-reload
sudo systemctl enable openhands.service
sudo systemctl start openhands.service

echo "=== Setup Complete ==="
echo "OpenHands will start automatically on system boot."
echo "To check status: sudo systemctl status openhands"
echo "To view logs: docker compose -f docker-compose-custom.yml logs -f"
echo "To restart: sudo systemctl restart openhands"