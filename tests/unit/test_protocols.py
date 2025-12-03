"""Unit tests for protocol implementations."""

import pytest
import asyncio
from datetime import datetime

from multiagent_orchestration.protocols.a2a_protocol import (
    A2AProtocol,
    A2AMessage,
    MessageType,
    MessagePriority
)
from multiagent_orchestration.protocols.mcp_protocol import (
    MCPProtocol,
    MCPAction,
    MCPStatus
)


class TestA2AProtocol:
    """Test A2A Protocol functionality."""
    
    @pytest.mark.asyncio
    async def test_send_message(self):
        """Test sending a message."""
        protocol = A2AProtocol()
        
        message = await protocol.send_message(
            sender_id="agent-1",
            recipient_id="agent-2",
            message_type=MessageType.REQUEST,
            payload={"test": "data"}
        )
        
        assert message.sender_id == "agent-1"
        assert message.recipient_id == "agent-2"
        assert message.message_type == MessageType.REQUEST
        assert message.payload == {"test": "data"}
        assert message.message_id in protocol.sent_messages
    
    @pytest.mark.asyncio
    async def test_message_handler_registration(self):
        """Test registering message handlers."""
        protocol = A2AProtocol()
        handled_messages = []
        
        async def handler(message: A2AMessage):
            handled_messages.append(message)
        
        protocol.register_handler(MessageType.REQUEST, handler)
        
        # Send and process a message
        await protocol.send_message(
            sender_id="agent-1",
            recipient_id="agent-2",
            message_type=MessageType.REQUEST,
            payload={"test": "data"}
        )
        
        message = await protocol.receive_message()
        await protocol._handle_message(message)
        
        assert len(handled_messages) == 1
        assert handled_messages[0].message_type == MessageType.REQUEST
    
    def test_message_history(self):
        """Test retrieving message history."""
        protocol = A2AProtocol()
        
        # Add some messages to history
        for i in range(5):
            msg = A2AMessage(
                sender_id=f"agent-{i}",
                recipient_id="agent-dest",
                message_type=MessageType.NOTIFICATION,
                payload={"index": i}
            )
            protocol.received_messages[msg.message_id] = msg
        
        history = protocol.get_message_history(limit=3)
        assert len(history) == 3


class TestMCPProtocol:
    """Test MCP Protocol functionality."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test agent initialization."""
        protocol = MCPProtocol(agent_id="agent-1", agent_type="test")
        
        message = await protocol.initialize(
            capabilities=["test_capability"],
            metadata={"test": "meta"}
        )
        
        assert message.action == MCPAction.INITIALIZE
        assert message.status == MCPStatus.READY
        assert protocol.context.status == MCPStatus.READY
        assert "test_capability" in protocol.context.capabilities
    
    @pytest.mark.asyncio
    async def test_context_update(self):
        """Test updating agent context."""
        protocol = MCPProtocol(agent_id="agent-1", agent_type="test")
        await protocol.initialize(capabilities=["test"])
        
        message = await protocol.update_context({
            "state": {"key": "value"},
            "metadata": {"updated": True}
        })
        
        assert message.action == MCPAction.UPDATE_CONTEXT
        assert protocol.context.state["key"] == "value"
        assert protocol.context.metadata["updated"] is True
    
    @pytest.mark.asyncio
    async def test_task_execution(self):
        """Test task execution tracking."""
        protocol = MCPProtocol(agent_id="agent-1", agent_type="test")
        await protocol.initialize(capabilities=["test"])
        
        message = await protocol.execute_task(
            task_id="task-1",
            task_type="test_task",
            task_data={"data": "value"}
        )
        
        assert message.action == MCPAction.EXECUTE_TASK
        assert protocol.context.status == MCPStatus.PROCESSING
        assert len(protocol.context.current_tasks) == 1
        assert protocol.context.current_tasks[0]["task_id"] == "task-1"
    
    @pytest.mark.asyncio
    async def test_task_completion(self):
        """Test completing a task."""
        protocol = MCPProtocol(agent_id="agent-1", agent_type="test")
        await protocol.initialize(capabilities=["test"])
        
        # Start a task
        await protocol.execute_task(
            task_id="task-1",
            task_type="test_task",
            task_data={"data": "value"}
        )
        
        # Complete the task
        await protocol.complete_task("task-1", {"result": "success"})
        
        assert len(protocol.context.current_tasks) == 0
        assert len(protocol.context.task_history) == 1
        assert protocol.context.task_history[0]["task_id"] == "task-1"
        assert protocol.context.status == MCPStatus.READY
    
    @pytest.mark.asyncio
    async def test_get_status(self):
        """Test getting agent status."""
        protocol = MCPProtocol(agent_id="agent-1", agent_type="test")
        await protocol.initialize(capabilities=["test"])
        
        message = await protocol.get_status()
        
        assert message.action == MCPAction.GET_STATUS
        assert message.result["status"] == MCPStatus.READY
        assert message.result["active_tasks"] == 0
    
    @pytest.mark.asyncio
    async def test_reset(self):
        """Test resetting agent state."""
        protocol = MCPProtocol(agent_id="agent-1", agent_type="test")
        await protocol.initialize(capabilities=["test"])
        
        # Add some state
        await protocol.update_context({"state": {"key": "value"}})
        await protocol.execute_task("task-1", "test", {})
        
        # Reset
        message = await protocol.reset()
        
        assert message.action == MCPAction.RESET
        assert protocol.context.status == MCPStatus.IDLE
        assert len(protocol.context.current_tasks) == 0
        assert protocol.context.state == {}
