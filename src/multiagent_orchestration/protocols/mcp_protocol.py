"""
MCP (Model Context Protocol) Implementation

This module implements the MCP protocol for managing agent context,
state, and model interactions in the orchestration system.
"""

import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MCPAction(str, Enum):
    """Actions supported by the MCP protocol."""
    
    INITIALIZE = "initialize"
    UPDATE_CONTEXT = "update_context"
    QUERY_CONTEXT = "query_context"
    EXECUTE_TASK = "execute_task"
    GET_STATUS = "get_status"
    RESET = "reset"
    TERMINATE = "terminate"


class MCPStatus(str, Enum):
    """Status states for MCP agents."""
    
    IDLE = "idle"
    INITIALIZING = "initializing"
    READY = "ready"
    PROCESSING = "processing"
    WAITING = "waiting"
    ERROR = "error"
    TERMINATED = "terminated"


class MCPMessage(BaseModel):
    """
    MCP Message format for context and model management.
    
    Attributes:
        message_id: Unique identifier for the message
        agent_id: ID of the agent
        action: The action to perform
        context: Current context data
        parameters: Action-specific parameters
        timestamp: When the message was created
        status: Current status of the agent
    """
    
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    action: MCPAction
    context: Dict[str, Any] = Field(default_factory=dict)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: MCPStatus = MCPStatus.IDLE
    result: Optional[Dict[str, Any]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentContext(BaseModel):
    """
    Context information for an agent.
    
    Attributes:
        agent_id: Unique identifier for the agent
        agent_type: Type of agent (chief, slave, department-specific)
        capabilities: List of capabilities the agent has
        current_tasks: Tasks currently being executed
        task_history: History of completed tasks
        state: Current state data
        metadata: Additional metadata
    """
    
    agent_id: str
    agent_type: str
    capabilities: List[str] = Field(default_factory=list)
    current_tasks: List[Dict[str, Any]] = Field(default_factory=list)
    task_history: List[Dict[str, Any]] = Field(default_factory=list)
    state: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    status: MCPStatus = MCPStatus.IDLE
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class MCPProtocol:
    """
    MCP Protocol handler for managing agent context and model interactions.
    
    This protocol provides a standardized way to manage agent state,
    context, and interactions with language models or other AI systems.
    """
    
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.context = AgentContext(
            agent_id=agent_id,
            agent_type=agent_type
        )
        self.message_history: List[MCPMessage] = []
        
    async def initialize(self, capabilities: List[str], metadata: Dict[str, Any] = None) -> MCPMessage:
        """
        Initialize the agent with its capabilities.
        
        Args:
            capabilities: List of agent capabilities
            metadata: Additional metadata
            
        Returns:
            MCPMessage with initialization result
        """
        self.context.capabilities = capabilities
        self.context.status = MCPStatus.INITIALIZING
        
        if metadata:
            self.context.metadata.update(metadata)
        
        message = MCPMessage(
            agent_id=self.agent_id,
            action=MCPAction.INITIALIZE,
            context=self.context.model_dump(),
            status=MCPStatus.READY
        )
        
        self.context.status = MCPStatus.READY
        self.context.last_updated = datetime.utcnow()
        self.message_history.append(message)
        
        return message
    
    async def update_context(self, updates: Dict[str, Any]) -> MCPMessage:
        """
        Update the agent's context.
        
        Args:
            updates: Dictionary of context updates
            
        Returns:
            MCPMessage with update result
        """
        # Update state
        if "state" in updates:
            self.context.state.update(updates["state"])
        
        # Update metadata
        if "metadata" in updates:
            self.context.metadata.update(updates["metadata"])
        
        # Update capabilities
        if "capabilities" in updates:
            self.context.capabilities.extend(updates["capabilities"])
        
        self.context.last_updated = datetime.utcnow()
        
        message = MCPMessage(
            agent_id=self.agent_id,
            action=MCPAction.UPDATE_CONTEXT,
            context=self.context.model_dump(),
            parameters=updates,
            status=self.context.status
        )
        
        self.message_history.append(message)
        return message
    
    async def query_context(self, query: Dict[str, Any]) -> MCPMessage:
        """
        Query the agent's context.
        
        Args:
            query: Query parameters
            
        Returns:
            MCPMessage with query results
        """
        result = {}
        
        if "field" in query:
            field = query["field"]
            if hasattr(self.context, field):
                result[field] = getattr(self.context, field)
        else:
            result = self.context.model_dump()
        
        message = MCPMessage(
            agent_id=self.agent_id,
            action=MCPAction.QUERY_CONTEXT,
            context=self.context.model_dump(),
            parameters=query,
            status=self.context.status,
            result=result
        )
        
        self.message_history.append(message)
        return message
    
    async def execute_task(
        self,
        task_id: str,
        task_type: str,
        task_data: Dict[str, Any]
    ) -> MCPMessage:
        """
        Execute a task and track it in context.
        
        Args:
            task_id: Unique identifier for the task
            task_type: Type of task
            task_data: Task-specific data
            
        Returns:
            MCPMessage with task execution status
        """
        task = {
            "task_id": task_id,
            "task_type": task_type,
            "data": task_data,
            "started_at": datetime.utcnow().isoformat(),
            "status": "in_progress"
        }
        
        self.context.current_tasks.append(task)
        self.context.status = MCPStatus.PROCESSING
        self.context.last_updated = datetime.utcnow()
        
        message = MCPMessage(
            agent_id=self.agent_id,
            action=MCPAction.EXECUTE_TASK,
            context=self.context.model_dump(),
            parameters={"task": task},
            status=MCPStatus.PROCESSING,
            result={"task_id": task_id, "status": "started"}
        )
        
        self.message_history.append(message)
        return message
    
    async def complete_task(self, task_id: str, result: Dict[str, Any]) -> None:
        """
        Mark a task as complete and move it to history.
        
        Args:
            task_id: ID of the completed task
            result: Task result data
        """
        # Find and remove task from current tasks
        task = None
        for i, t in enumerate(self.context.current_tasks):
            if t["task_id"] == task_id:
                task = self.context.current_tasks.pop(i)
                break
        
        if task:
            task["status"] = "completed"
            task["completed_at"] = datetime.utcnow().isoformat()
            task["result"] = result
            self.context.task_history.append(task)
        
        # Update status
        if not self.context.current_tasks:
            self.context.status = MCPStatus.READY
        
        self.context.last_updated = datetime.utcnow()
    
    async def get_status(self) -> MCPMessage:
        """
        Get the current status of the agent.
        
        Returns:
            MCPMessage with status information
        """
        message = MCPMessage(
            agent_id=self.agent_id,
            action=MCPAction.GET_STATUS,
            context=self.context.model_dump(),
            status=self.context.status,
            result={
                "status": self.context.status,
                "active_tasks": len(self.context.current_tasks),
                "completed_tasks": len(self.context.task_history)
            }
        )
        
        self.message_history.append(message)
        return message
    
    async def reset(self) -> MCPMessage:
        """
        Reset the agent to initial state.
        
        Returns:
            MCPMessage with reset confirmation
        """
        self.context.current_tasks = []
        self.context.state = {}
        self.context.status = MCPStatus.IDLE
        self.context.last_updated = datetime.utcnow()
        
        message = MCPMessage(
            agent_id=self.agent_id,
            action=MCPAction.RESET,
            context=self.context.model_dump(),
            status=MCPStatus.IDLE
        )
        
        self.message_history.append(message)
        return message
    
    def get_context(self) -> AgentContext:
        """Get the current agent context."""
        return self.context
    
    def get_message_history(self, limit: Optional[int] = None) -> List[MCPMessage]:
        """
        Get the message history.
        
        Args:
            limit: Maximum number of messages to return
            
        Returns:
            List of MCP messages
        """
        messages = self.message_history.copy()
        messages.reverse()  # Most recent first
        
        if limit:
            messages = messages[:limit]
        
        return messages
