"""
Base Agent Implementation

Provides the foundation for all agent types in the orchestration system.
"""

import asyncio
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..protocols.a2a_protocol import (
    A2AProtocol,
    A2AMessage,
    MessageType,
    MessagePriority
)
from ..protocols.mcp_protocol import MCPProtocol, MCPStatus


class BaseAgent(ABC):
    """
    Base class for all agents in the orchestration system.
    
    Provides common functionality for MCP-powered agents with A2A communication.
    """
    
    def __init__(
        self,
        agent_id: Optional[str] = None,
        agent_type: str = "base",
        capabilities: Optional[List[str]] = None
    ):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.agent_type = agent_type
        self.capabilities = capabilities or []
        
        # Initialize protocols
        self.mcp = MCPProtocol(self.agent_id, self.agent_type)
        self.a2a = A2AProtocol()
        
        # State
        self.is_initialized = False
        self.is_running = False
        self.tasks: Dict[str, Dict[str, Any]] = {}
        
    async def initialize(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the agent.
        
        Args:
            metadata: Additional initialization metadata
        """
        await self.mcp.initialize(self.capabilities, metadata or {})
        
        # Register A2A message handlers
        self._register_message_handlers()
        
        self.is_initialized = True
        print(f"[{self.agent_type}:{self.agent_id}] Initialized with capabilities: {self.capabilities}")
    
    def _register_message_handlers(self) -> None:
        """Register handlers for different message types."""
        self.a2a.register_handler(MessageType.REQUEST, self._handle_request)
        self.a2a.register_handler(MessageType.TASK_ASSIGNMENT, self._handle_task_assignment)
        self.a2a.register_handler(MessageType.BROADCAST, self._handle_broadcast)
        self.a2a.register_handler(MessageType.STATUS_UPDATE, self._handle_status_update)
    
    async def start(self) -> None:
        """Start the agent's message processing loop."""
        if not self.is_initialized:
            await self.initialize()
        
        self.is_running = True
        print(f"[{self.agent_type}:{self.agent_id}] Started")
        
        # Start A2A message processing in background
        asyncio.create_task(self.a2a.process_messages())
    
    async def stop(self) -> None:
        """Stop the agent."""
        self.is_running = False
        self.a2a.stop()
        print(f"[{self.agent_type}:{self.agent_id}] Stopped")
    
    async def send_message(
        self,
        recipient_id: Optional[str],
        message_type: MessageType,
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL
    ) -> A2AMessage:
        """
        Send a message to another agent.
        
        Args:
            recipient_id: ID of recipient agent (None for broadcast)
            message_type: Type of message
            payload: Message content
            priority: Message priority
            
        Returns:
            The sent message
        """
        return await self.a2a.send_message(
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            message_type=message_type,
            payload=payload,
            priority=priority
        )
    
    async def _handle_request(self, message: A2AMessage) -> None:
        """
        Handle incoming request messages.
        
        Args:
            message: The request message
        """
        print(f"[{self.agent_type}:{self.agent_id}] Received request: {message.payload.get('request_type')}")
        
        # Process the request
        result = await self.process_request(message.payload)
        
        # Send response
        await self.send_message(
            recipient_id=message.sender_id,
            message_type=MessageType.RESPONSE,
            payload={
                "request_id": message.message_id,
                "result": result
            }
        )
    
    async def _handle_task_assignment(self, message: A2AMessage) -> None:
        """
        Handle task assignment messages.
        
        Args:
            message: The task assignment message
        """
        task_data = message.payload
        task_id = task_data.get("task_id", str(uuid.uuid4()))
        
        print(f"[{self.agent_type}:{self.agent_id}] Received task: {task_id}")
        
        # Track task in MCP
        await self.mcp.execute_task(
            task_id=task_id,
            task_type=task_data.get("task_type", "unknown"),
            task_data=task_data
        )
        
        # Execute the task
        try:
            result = await self.execute_task(task_data)
            
            # Mark task as complete
            await self.mcp.complete_task(task_id, result)
            
            # Notify completion
            await self.send_message(
                recipient_id=message.sender_id,
                message_type=MessageType.TASK_COMPLETION,
                payload={
                    "task_id": task_id,
                    "status": "completed",
                    "result": result
                }
            )
        except Exception as e:
            print(f"[{self.agent_type}:{self.agent_id}] Task {task_id} failed: {e}")
            await self.send_message(
                recipient_id=message.sender_id,
                message_type=MessageType.ERROR,
                payload={
                    "task_id": task_id,
                    "error": str(e)
                }
            )
    
    async def _handle_broadcast(self, message: A2AMessage) -> None:
        """
        Handle broadcast messages.
        
        Args:
            message: The broadcast message
        """
        print(f"[{self.agent_type}:{self.agent_id}] Received broadcast: {message.payload.get('subject')}")
        await self.process_broadcast(message.payload)
    
    async def _handle_status_update(self, message: A2AMessage) -> None:
        """
        Handle status update messages.
        
        Args:
            message: The status update message
        """
        print(f"[{self.agent_type}:{self.agent_id}] Status update from {message.sender_id}")
    
    @abstractmethod
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request message. Must be implemented by subclasses.
        
        Args:
            request: Request data
            
        Returns:
            Response data
        """
        pass
    
    @abstractmethod
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task. Must be implemented by subclasses.
        
        Args:
            task_data: Task information
            
        Returns:
            Task result
        """
        pass
    
    async def process_broadcast(self, broadcast: Dict[str, Any]) -> None:
        """
        Process a broadcast message. Can be overridden by subclasses.
        
        Args:
            broadcast: Broadcast data
        """
        pass
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent.
        
        Returns:
            Status information
        """
        mcp_status = await self.mcp.get_status()
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": mcp_status.status,
            "capabilities": self.capabilities,
            "is_running": self.is_running,
            "result": mcp_status.result
        }
