"""
Redis Service for real-time event publishing and SSE.

This module provides Redis-based event publishing and subscription
for Server-Sent Events (SSE) and real-time updates.
"""

import asyncio
import json
import logging
from typing import AsyncGenerator, Dict, Any, Optional
import redis.asyncio as redis

logger = logging.getLogger(__name__)


class RedisService:
    """Redis service for event publishing and SSE."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        """
        Initialize Redis service.
        
        Args:
            redis_url: Redis connection URL
        """
        self.redis_url = redis_url
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
    
    async def connect(self):
        """Connect to Redis."""
        try:
            self.redis_client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis_client.ping()
            logger.info(f"Connected to Redis at {self.redis_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Disconnected from Redis")
    
    async def publish_search_event(self, search_id: str, event_type: str, data: Dict[str, Any]):
        """
        Publish a search event to Redis channel.
        
        Args:
            search_id: Search request ID
            event_type: Type of event (status, progress, error, etc.)
            data: Event data
        """
        if not self.redis_client:
            await self.connect()
        
        try:
            channel = f"search:{search_id}"
            event = {
                "event": event_type,
                "data": data,
                "search_id": search_id
            }
            
            await self.redis_client.publish(channel, json.dumps(event))
            logger.debug(f"Published event to {channel}: {event_type}")
            
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
    
    async def subscribe_to_search(self, search_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Subscribe to search events and yield them as they arrive.
        
        Args:
            search_id: Search request ID
            
        Yields:
            Event data dictionaries
        """
        if not self.redis_client:
            await self.connect()
        
        channel = f"search:{search_id}"
        self.pubsub = self.redis_client.pubsub()
        
        try:
            # Subscribe to the channel
            await self.pubsub.subscribe(channel)
            logger.info(f"Subscribed to channel: {channel}")
            
            # Listen for messages
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    try:
                        event_data = json.loads(message["data"])
                        yield event_data
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse message: {e}")
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                
                elif message["type"] == "subscribe":
                    logger.debug(f"Subscribed to {message['channel']}")
                
                elif message["type"] == "unsubscribe":
                    logger.debug(f"Unsubscribed from {message['channel']}")
                    break
        
        except asyncio.CancelledError:
            logger.info(f"Subscription cancelled for {channel}")
            raise
        
        except Exception as e:
            logger.error(f"Error in subscription: {e}")
            raise
        
        finally:
            if self.pubsub:
                await self.pubsub.unsubscribe(channel)
                await self.pubsub.close()
    
    async def get_search_status(self, search_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current search status from Redis.
        
        Args:
            search_id: Search request ID
            
        Returns:
            Current status or None if not found
        """
        if not self.redis_client:
            await self.connect()
        
        try:
            key = f"search:status:{search_id}"
            status_json = await self.redis_client.get(key)
            
            if status_json:
                return json.loads(status_json)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get search status: {e}")
            return None
    
    async def set_search_status(self, search_id: str, status: Dict[str, Any], ttl: int = 3600):
        """
        Set search status in Redis with TTL.
        
        Args:
            search_id: Search request ID
            status: Status data
            ttl: Time to live in seconds (default: 1 hour)
        """
        if not self.redis_client:
            await self.connect()
        
        try:
            key = f"search:status:{search_id}"
            await self.redis_client.setex(key, ttl, json.dumps(status))
            logger.debug(f"Set status for {search_id}")
            
        except Exception as e:
            logger.error(f"Failed to set search status: {e}")
    
    async def cleanup_search_data(self, search_id: str):
        """
        Clean up Redis data for a search.
        
        Args:
            search_id: Search request ID
        """
        if not self.redis_client:
            await self.connect()
        
        try:
            # Delete status key
            status_key = f"search:status:{search_id}"
            await self.redis_client.delete(status_key)
            
            # Note: We don't delete the channel as it might still have subscribers
            logger.info(f"Cleaned up Redis data for {search_id}")
            
        except Exception as e:
            logger.error(f"Failed to cleanup search data: {e}")


# Global Redis service instance
_redis_service: Optional[RedisService] = None


async def get_redis_service() -> RedisService:
    """Get or create Redis service instance."""
    global _redis_service
    
    if _redis_service is None:
        _redis_service = RedisService()
        await _redis_service.connect()
    
    return _redis_service


async def publish_search_progress(search_id: str, processed: int, total: int, message: str = ""):
    """Publish search progress event."""
    try:
        redis_service = await get_redis_service()
        
        data = {
            "processed": processed,
            "total": total,
            "percentage": (processed / total * 100) if total > 0 else 0,
            "message": message
        }
        
        await redis_service.publish_search_event(search_id, "progress", data)
        
        # Also update status
        status_data = {
            "search_id": search_id,
            "status": "PROCESSING",
            "progress": data,
            "timestamp": asyncio.get_event_loop().time()
        }
        await redis_service.set_search_status(search_id, status_data)
        
    except Exception as e:
        logger.error(f"Failed to publish progress: {e}")


async def publish_search_status(search_id: str, status: str, message: str = "", data: Dict[str, Any] = None):
    """Publish search status event."""
    try:
        redis_service = await get_redis_service()
        
        event_data = {
            "status": status,
            "message": message,
            "search_id": search_id
        }
        
        if data:
            event_data.update(data)
        
        await redis_service.publish_search_event(search_id, "status", event_data)
        
        # Update status in Redis
        status_data = {
            "search_id": search_id,
            "status": status,
            "message": message,
            "data": data or {},
            "timestamp": asyncio.get_event_loop().time()
        }
        await redis_service.set_search_status(search_id, status_data)
        
    except Exception as e:
        logger.error(f"Failed to publish status: {e}")


async def publish_search_error(search_id: str, error: str, details: Dict[str, Any] = None):
    """Publish search error event."""
    try:
        redis_service = await get_redis_service()
        
        data = {
            "error": error,
            "search_id": search_id
        }
        
        if details:
            data["details"] = details
        
        await redis_service.publish_search_event(search_id, "error", data)
        
        # Update error status
        status_data = {
            "search_id": search_id,
            "status": "ERROR",
            "error": error,
            "details": details or {},
            "timestamp": asyncio.get_event_loop().time()
        }
        await redis_service.set_search_status(search_id, status_data)
        
    except Exception as e:
        logger.error(f"Failed to publish error: {e}")