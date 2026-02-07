import requests
import json
import time

BASE_URL = "http://localhost:3000/api"

def test_health():
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health status: {response.status_code}")
    return response.status_code == 200

def create_conversation():
    print("Creating conversation...")
    response = requests.post(f"{BASE_URL}/v1/conversations", json={
        "title": "Test Conversation",
        "description": "Testing OpenHands API"
    })
    print(f"Create conversation status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Conversation created: {data['id']}")
        return data['id']
    return None

def send_message(conversation_id):
    print(f"Sending message to conversation {conversation_id}...")
    response = requests.post(f"{BASE_URL}/v1/conversations/{conversation_id}/messages", json={
        "content": "Кто ты?",
        "role": "user"
    })
    print(f"Send message status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Message sent: {data['id']}")
        return data['id']
    return None

def get_messages(conversation_id):
    print(f"Getting messages for conversation {conversation_id}...")
    response = requests.get(f"{BASE_URL}/v1/conversations/{conversation_id}/messages")
    print(f"Get messages status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total messages: {len(data)}")
        for msg in data:
            print(f"  - {msg['role']}: {msg['content'][:100]}...")
        return data
    return []

def main():
    print("=== OpenHands API Test ===")
    
    # Test health
    if not test_health():
        print("Health check failed!")
        return
    
    # Create conversation
    conv_id = create_conversation()
    if not conv_id:
        print("Failed to create conversation!")
        return
    
    # Send message
    msg_id = send_message(conv_id)
    if not msg_id:
        print("Failed to send message!")
        return
    
    # Wait for response
    print("Waiting for AI response...")
    time.sleep(5)
    
    # Get messages
    messages = get_messages(conv_id)
    
    # Check if we got AI response
    ai_messages = [m for m in messages if m.get('role') == 'assistant']
    if ai_messages:
        print(f"\n✅ SUCCESS: Got AI response!")
        print(f"Response: {ai_messages[0]['content'][:200]}...")
    else:
        print("\n❌ FAILED: No AI response received")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()