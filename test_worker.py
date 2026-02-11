#!/usr/bin/env python3
"""Test script to verify Celery worker functionality."""
import os
import sys
import time
import uuid
from celery import Celery

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create a simple Celery app for testing
test_app = Celery(
    "test_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

test_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@test_app.task
def test_task(task_id: str):
    """Simple test task."""
    print(f"Test task {task_id} started")
    time.sleep(2)
    print(f"Test task {task_id} completed")
    return {"status": "completed", "task_id": task_id}

if __name__ == "__main__":
    # Test sending a task
    task_id = str(uuid.uuid4())
    print(f"Sending test task with ID: {task_id}")
    result = test_task.delay(task_id)
    
    print(f"Task sent. Result ID: {result.id}")
    print("Waiting for task to complete...")
    
    # Wait for result
    try:
        task_result = result.get(timeout=10)
        print(f"Task completed successfully: {task_result}")
    except Exception as e:
        print(f"Error getting task result: {e}")
    
    print("Test completed")