#!/bin/bash

# Start mock inventory service (Service Beta) on port 5002
echo "Starting Mock Inventory Service (Service Beta) on port 5002..."
python mock_inventory.py > inventory.log 2>&1 &
INVENTORY_PID=$!
echo "Inventory service started with PID: $INVENTORY_PID"

# Wait a moment for inventory service to start
sleep 2

# Start Service Alpha on port 5001
echo "Starting Service Alpha on port 5001..."
python app.py > service_alpha.log 2>&1 &
SERVICE_ALPHA_PID=$!
echo "Service Alpha started with PID: $SERVICE_ALPHA_PID"

# Wait for services to start
sleep 3

echo "Services started successfully!"
echo "Inventory service log: inventory.log"
echo "Service Alpha log: service_alpha.log"
echo ""
echo "To test the system, run: curl http://localhost:5001/order/item_001"
echo "To stop services, run: kill $INVENTORY_PID $SERVICE_ALPHA_PID"