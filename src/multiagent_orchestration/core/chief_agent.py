"""
Chief Agent Implementation

The Chief Agent is the orchestrator that coordinates all slave agents
and manages the overall system operation.
"""

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime

from .base_agent import BaseAgent
from ..protocols.a2a_protocol import MessageType, MessagePriority


class ChiefAgent(BaseAgent):
    """
    Chief Agent - The master orchestrator of the multi-agent system.
    
    Responsibilities:
    - Coordinate all slave agents
    - Assign tasks to appropriate agents
    - Monitor system health and status
    - Handle escalations and complex decisions
    - Manage inter-departmental coordination
    """
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            agent_type="chief",
            capabilities=[
                "task_orchestration",
                "agent_coordination",
                "system_monitoring",
                "decision_making",
                "resource_allocation",
                "escalation_handling"
            ]
        )
        
        # Registry of slave agents
        self.slave_agents: Dict[str, Dict[str, Any]] = {}
        
        # Task queue and assignments
        self.pending_tasks: List[Dict[str, Any]] = []
        self.active_assignments: Dict[str, Dict[str, Any]] = {}
        
    async def initialize(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the Chief Agent."""
        await super().initialize(metadata or {
            "role": "chief",
            "authority_level": "highest"
        })
        print(f"[ChiefAgent:{self.agent_id}] Chief Agent initialized and ready to orchestrate")
    
    async def register_slave_agent(
        self,
        agent_id: str,
        agent_type: str,
        capabilities: List[str]
    ) -> Dict[str, Any]:
        """
        Register a slave agent with the chief.
        
        Args:
            agent_id: ID of the slave agent
            agent_type: Type of agent (e.g., 'hr', 'finance', 'support')
            capabilities: List of agent capabilities
            
        Returns:
            Registration confirmation
        """
        self.slave_agents[agent_id] = {
            "agent_id": agent_id,
            "agent_type": agent_type,
            "capabilities": capabilities,
            "status": "registered",
            "registered_at": datetime.utcnow().isoformat(),
            "tasks_assigned": 0,
            "tasks_completed": 0
        }
        
        print(f"[ChiefAgent:{self.agent_id}] Registered slave agent: {agent_type}:{agent_id}")
        
        # Send welcome message
        await self.send_message(
            recipient_id=agent_id,
            message_type=MessageType.NOTIFICATION,
            payload={
                "subject": "registration_confirmed",
                "message": "You have been registered with the Chief Agent",
                "chief_id": self.agent_id
            }
        )
        
        return {
            "status": "success",
            "agent_id": agent_id,
            "chief_id": self.agent_id
        }
    
    async def assign_task(
        self,
        task_id: str,
        task_type: str,
        task_data: Dict[str, Any],
        required_capabilities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Assign a task to the most suitable slave agent.
        
        Args:
            task_id: Unique task identifier
            task_type: Type of task
            task_data: Task information
            required_capabilities: Required agent capabilities
            
        Returns:
            Assignment result
        """
        # Find suitable agent
        suitable_agent = self._find_suitable_agent(required_capabilities or [])
        
        if not suitable_agent:
            print(f"[ChiefAgent:{self.agent_id}] No suitable agent found for task {task_id}")
            return {
                "status": "failed",
                "reason": "no_suitable_agent",
                "task_id": task_id
            }
        
        agent_id = suitable_agent["agent_id"]
        
        # Create task assignment
        assignment = {
            "task_id": task_id,
            "task_type": task_type,
            "assigned_to": agent_id,
            "assigned_at": datetime.utcnow().isoformat(),
            "status": "assigned",
            "data": task_data
        }
        
        self.active_assignments[task_id] = assignment
        self.slave_agents[agent_id]["tasks_assigned"] += 1
        
        # Send task to agent
        await self.send_message(
            recipient_id=agent_id,
            message_type=MessageType.TASK_ASSIGNMENT,
            payload={
                "task_id": task_id,
                "task_type": task_type,
                **task_data
            },
            priority=task_data.get("priority", MessagePriority.NORMAL)
        )
        
        print(f"[ChiefAgent:{self.agent_id}] Assigned task {task_id} to {suitable_agent['agent_type']}:{agent_id}")
        
        return {
            "status": "success",
            "task_id": task_id,
            "assigned_to": agent_id,
            "agent_type": suitable_agent["agent_type"]
        }
    
    def _find_suitable_agent(self, required_capabilities: List[str]) -> Optional[Dict[str, Any]]:
        """
        Find the most suitable agent for a task based on capabilities.
        
        Args:
            required_capabilities: Required capabilities
            
        Returns:
            Agent information or None
        """
        suitable_agents = []
        
        for agent_id, agent_info in self.slave_agents.items():
            # Check if agent has all required capabilities
            if all(cap in agent_info["capabilities"] for cap in required_capabilities):
                suitable_agents.append(agent_info)
        
        if not suitable_agents:
            return None
        
        # Return agent with least active tasks (load balancing)
        return min(
            suitable_agents,
            key=lambda a: a["tasks_assigned"] - a["tasks_completed"]
        )
    
    async def broadcast_to_all_agents(
        self,
        subject: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Broadcast a message to all slave agents.
        
        Args:
            subject: Message subject
            message: Message content
            data: Additional data
        """
        await self.send_message(
            recipient_id=None,  # Broadcast to all
            message_type=MessageType.BROADCAST,
            payload={
                "subject": subject,
                "message": message,
                "data": data or {},
                "from_chief": True
            }
        )
        
        print(f"[ChiefAgent:{self.agent_id}] Broadcast: {subject}")
    
    async def get_system_status(self) -> Dict[str, Any]:
        """
        Get overall system status.
        
        Returns:
            System status information
        """
        total_tasks = len(self.active_assignments)
        completed_tasks = sum(
            1 for assignment in self.active_assignments.values()
            if assignment["status"] == "completed"
        )
        
        return {
            "chief_agent": await self.get_status(),
            "slave_agents": {
                "total": len(self.slave_agents),
                "registered": list(self.slave_agents.values())
            },
            "tasks": {
                "total_assigned": total_tasks,
                "completed": completed_tasks,
                "active": total_tasks - completed_tasks
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request to the Chief Agent.
        
        Args:
            request: Request data
            
        Returns:
            Response data
        """
        request_type = request.get("request_type")
        
        if request_type == "assign_task":
            return await self.assign_task(
                task_id=request.get("task_id"),
                task_type=request.get("task_type"),
                task_data=request.get("task_data", {}),
                required_capabilities=request.get("required_capabilities")
            )
        
        elif request_type == "get_status":
            return await self.get_system_status()
        
        elif request_type == "register_agent":
            return await self.register_slave_agent(
                agent_id=request.get("agent_id"),
                agent_type=request.get("agent_type"),
                capabilities=request.get("capabilities", [])
            )
        
        else:
            return {
                "status": "error",
                "message": f"Unknown request type: {request_type}"
            }
    
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task directly (for high-priority chief-level tasks).
        
        Args:
            task_data: Task information
            
        Returns:
            Task result
        """
        task_type = task_data.get("task_type")
        
        print(f"[ChiefAgent:{self.agent_id}] Executing chief-level task: {task_type}")
        
        # Chief-level task execution logic
        if task_type == "orchestrate":
            # Orchestrate multiple slave agents
            return {"status": "orchestrated", "message": "Multi-agent coordination initiated"}
        
        elif task_type == "escalation":
            # Handle escalated issue
            return {"status": "handled", "message": "Escalation resolved by chief"}
        
        else:
            return {"status": "completed", "message": f"Chief task {task_type} completed"}
    
    async def handle_task_completion(self, message: Any) -> None:
        """
        Handle task completion notifications from slave agents.
        
        Args:
            message: Task completion message
        """
        task_id = message.payload.get("task_id")
        
        if task_id in self.active_assignments:
            assignment = self.active_assignments[task_id]
            assignment["status"] = "completed"
            assignment["completed_at"] = datetime.utcnow().isoformat()
            assignment["result"] = message.payload.get("result")
            
            # Update agent stats
            agent_id = assignment["assigned_to"]
            if agent_id in self.slave_agents:
                self.slave_agents[agent_id]["tasks_completed"] += 1
            
            print(f"[ChiefAgent:{self.agent_id}] Task {task_id} completed by {agent_id}")
