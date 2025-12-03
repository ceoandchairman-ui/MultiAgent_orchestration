"""
Slave Agent Implementation

Slave agents are specialized agents that execute tasks assigned by the Chief Agent.
"""

from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent
from ..protocols.a2a_protocol import MessageType


class SlaveAgent(BaseAgent):
    """
    Slave Agent - Specialized agents that execute assigned tasks.
    
    Responsibilities:
    - Register with the Chief Agent
    - Execute assigned tasks
    - Report status and results
    - Handle department-specific operations
    """
    
    def __init__(
        self,
        agent_id: Optional[str] = None,
        agent_type: str = "slave",
        department: str = "general",
        capabilities: Optional[List[str]] = None
    ):
        super().__init__(
            agent_id=agent_id,
            agent_type=agent_type,
            capabilities=capabilities or []
        )
        
        self.department = department
        self.chief_agent_id: Optional[str] = None
        self.is_registered = False
        
    async def initialize(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the Slave Agent."""
        meta = metadata or {}
        meta.update({
            "department": self.department,
            "role": "slave"
        })
        
        await super().initialize(meta)
        print(f"[SlaveAgent:{self.agent_id}] Slave agent initialized for department: {self.department}")
    
    async def register_with_chief(self, chief_agent_id: str) -> Dict[str, Any]:
        """
        Register this slave agent with the Chief Agent.
        
        Args:
            chief_agent_id: ID of the Chief Agent
            
        Returns:
            Registration result
        """
        self.chief_agent_id = chief_agent_id
        
        # Send registration request
        message = await self.send_message(
            recipient_id=chief_agent_id,
            message_type=MessageType.REQUEST,
            payload={
                "request_type": "register_agent",
                "agent_id": self.agent_id,
                "agent_type": self.agent_type,
                "department": self.department,
                "capabilities": self.capabilities
            }
        )
        
        self.is_registered = True
        print(f"[SlaveAgent:{self.agent_id}] Registered with Chief Agent: {chief_agent_id}")
        
        return {
            "status": "success",
            "chief_id": chief_agent_id,
            "agent_id": self.agent_id
        }
    
    async def report_status_to_chief(self) -> None:
        """Report current status to the Chief Agent."""
        if not self.chief_agent_id:
            print(f"[SlaveAgent:{self.agent_id}] Not registered with any chief")
            return
        
        status = await self.get_status()
        
        await self.send_message(
            recipient_id=self.chief_agent_id,
            message_type=MessageType.STATUS_UPDATE,
            payload={
                "agent_id": self.agent_id,
                "department": self.department,
                "status": status
            }
        )
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request message.
        
        Args:
            request: Request data
            
        Returns:
            Response data
        """
        request_type = request.get("request_type")
        
        if request_type == "get_capabilities":
            return {
                "capabilities": self.capabilities,
                "department": self.department
            }
        
        elif request_type == "health_check":
            return {
                "status": "healthy",
                "agent_id": self.agent_id
            }
        
        else:
            return await self._process_department_request(request)
    
    async def _process_department_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process department-specific requests.
        Override in department-specific agents.
        
        Args:
            request: Request data
            
        Returns:
            Response data
        """
        return {
            "status": "processed",
            "department": self.department,
            "message": f"Request processed by {self.department} department"
        }
    
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an assigned task.
        
        Args:
            task_data: Task information
            
        Returns:
            Task result
        """
        task_type = task_data.get("task_type")
        task_id = task_data.get("task_id")
        
        print(f"[SlaveAgent:{self.agent_id}] Executing task {task_id}: {task_type}")
        
        # Execute based on task type
        result = await self._execute_department_task(task_type, task_data)
        
        return result
    
    async def _execute_department_task(
        self,
        task_type: str,
        task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute department-specific task.
        Override in department-specific agents.
        
        Args:
            task_type: Type of task
            task_data: Task information
            
        Returns:
            Task result
        """
        return {
            "status": "completed",
            "department": self.department,
            "task_type": task_type,
            "message": f"Task executed by {self.department} department"
        }
    
    async def process_broadcast(self, broadcast: Dict[str, Any]) -> None:
        """
        Process broadcast messages.
        
        Args:
            broadcast: Broadcast data
        """
        subject = broadcast.get("subject")
        message = broadcast.get("message")
        
        print(f"[SlaveAgent:{self.agent_id}] Broadcast received: {subject} - {message}")
        
        # Handle specific broadcasts
        if subject == "system_shutdown":
            await self.stop()
        elif subject == "status_check":
            await self.report_status_to_chief()
