"""
A2A (Agent-to-Agent) Protocol Implementation

This module implements the A2A protocol for seamless communication between agents
in the multi-agent orchestration system.
"""

import asyncio
import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, List, Callable
from pydantic import BaseModel, Field


class MessageType(str, Enum):
    """Types of messages in the A2A protocol."""
    
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    NOTIFICATION = "notification"
    TASK_ASSIGNMENT = "task_assignment"
    TASK_COMPLETION = "task_completion"
    STATUS_UPDATE = "status_update"
    ERROR = "error"


class MessagePriority(str, Enum):
    """Priority levels for messages."""
    
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class A2AMessage(BaseModel):
    """
    A2A Message format for agent-to-agent communication.
    
    Attributes:
        message_id: Unique identifier for the message
        sender_id: ID of the sending agent
        recipient_id: ID of the receiving agent (None for broadcast)
        message_type: Type of the message
        priority: Priority level of the message
        payload: The actual message content
        timestamp: When the message was created
        metadata: Additional metadata about the message
    """
    
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str
    recipient_id: Optional[str] = None
    message_type: MessageType
    priority: MessagePriority = MessagePriority.NORMAL
    payload: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: Optional[str] = None  # For tracking related messages
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class A2AProtocol:
    """
    A2A Protocol handler for managing agent-to-agent communication.
    
    This protocol ensures reliable, ordered, and efficient message passing
    between agents in the orchestration system.
    """
    
    def __init__(self):
        self.message_handlers: Dict[MessageType, List[Callable]] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.sent_messages: Dict[str, A2AMessage] = {}
        self.received_messages: Dict[str, A2AMessage] = {}
        self.is_running = False
        
    def register_handler(
        self,
        message_type: MessageType,
        handler: Callable[[A2AMessage], Any]
    ) -> None:
        """
        Register a handler function for a specific message type.
        
        Args:
            message_type: The type of message to handle
            handler: Async function to call when message is received
        """
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)
    
    async def send_message(
        self,
        sender_id: str,
        recipient_id: Optional[str],
        message_type: MessageType,
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
        correlation_id: Optional[str] = None
    ) -> A2AMessage:
        """
        Send a message from one agent to another.
        
        Args:
            sender_id: ID of the sending agent
            recipient_id: ID of the receiving agent (None for broadcast)
            message_type: Type of message
            payload: Message content
            priority: Priority level
            correlation_id: ID to correlate with previous messages
            
        Returns:
            The created A2AMessage
        """
        message = A2AMessage(
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_type=message_type,
            payload=payload,
            priority=priority,
            correlation_id=correlation_id
        )
        
        self.sent_messages[message.message_id] = message
        await self.message_queue.put(message)
        
        return message
    
    async def receive_message(self) -> A2AMessage:
        """
        Receive the next message from the queue.
        
        Returns:
            The next A2AMessage in the queue
        """
        message = await self.message_queue.get()
        self.received_messages[message.message_id] = message
        return message
    
    async def process_messages(self) -> None:
        """
        Continuously process messages from the queue.
        This should be run as a background task.
        """
        self.is_running = True
        while self.is_running:
            try:
                message = await self.receive_message()
                await self._handle_message(message)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error processing message: {e}")
    
    async def _handle_message(self, message: A2AMessage) -> None:
        """
        Route a message to its registered handlers.
        
        Args:
            message: The message to handle
        """
        handlers = self.message_handlers.get(message.message_type, [])
        
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(message)
                else:
                    handler(message)
            except Exception as e:
                print(f"Handler error for {message.message_type}: {e}")
    
    def stop(self) -> None:
        """Stop the message processing loop."""
        self.is_running = False
    
    def get_message_history(
        self,
        limit: Optional[int] = None,
        message_type: Optional[MessageType] = None
    ) -> List[A2AMessage]:
        """
        Get message history with optional filtering.
        
        Args:
            limit: Maximum number of messages to return
            message_type: Filter by message type
            
        Returns:
            List of messages
        """
        messages = list(self.received_messages.values())
        
        if message_type:
            messages = [m for m in messages if m.message_type == message_type]
        
        # Sort by timestamp (most recent first)
        messages.sort(key=lambda m: m.timestamp, reverse=True)
        
        if limit:
            messages = messages[:limit]
        
        return messages
