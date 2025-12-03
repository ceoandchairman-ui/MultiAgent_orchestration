"""HR Agent - Handles Human Resources operations."""

from typing import Any, Dict, Optional

from ..core.slave_agent import SlaveAgent


class HRAgent(SlaveAgent):
    """
    HR Agent - Specialized agent for Human Resources operations.
    
    Capabilities:
    - Employee onboarding
    - Leave management
    - Performance reviews
    - Policy queries
    - Training coordination
    """
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            agent_type="hr",
            department="hr",
            capabilities=[
                "employee_onboarding",
                "leave_management",
                "performance_reviews",
                "policy_queries",
                "training_coordination",
                "benefits_management"
            ]
        )
    
    async def _process_department_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process HR-specific requests."""
        request_type = request.get("request_type")
        
        if request_type == "employee_query":
            return await self._handle_employee_query(request)
        
        elif request_type == "leave_request":
            return await self._handle_leave_request(request)
        
        elif request_type == "policy_query":
            return await self._handle_policy_query(request)
        
        else:
            return await super()._process_department_request(request)
    
    async def _execute_department_task(
        self,
        task_type: str,
        task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute HR-specific tasks."""
        
        if task_type == "onboard_employee":
            return await self._onboard_employee(task_data)
        
        elif task_type == "process_leave":
            return await self._process_leave(task_data)
        
        elif task_type == "schedule_review":
            return await self._schedule_review(task_data)
        
        elif task_type == "coordinate_training":
            return await self._coordinate_training(task_data)
        
        else:
            return await super()._execute_department_task(task_type, task_data)
    
    async def _handle_employee_query(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle employee information queries."""
        employee_id = request.get("employee_id")
        query_type = request.get("query_type")
        
        return {
            "status": "success",
            "employee_id": employee_id,
            "query_type": query_type,
            "result": f"Employee information retrieved for {employee_id}"
        }
    
    async def _handle_leave_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle leave requests."""
        employee_id = request.get("employee_id")
        leave_type = request.get("leave_type")
        dates = request.get("dates")
        
        return {
            "status": "approved",
            "employee_id": employee_id,
            "leave_type": leave_type,
            "dates": dates,
            "message": "Leave request processed successfully"
        }
    
    async def _handle_policy_query(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle policy-related queries."""
        policy_category = request.get("policy_category")
        
        return {
            "status": "success",
            "policy_category": policy_category,
            "information": f"Policy information for {policy_category} retrieved"
        }
    
    async def _onboard_employee(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Onboard a new employee."""
        employee_name = task_data.get("employee_name")
        department = task_data.get("department")
        
        return {
            "status": "completed",
            "employee_name": employee_name,
            "department": department,
            "message": f"Employee {employee_name} onboarded to {department} successfully",
            "next_steps": ["IT setup", "Manager introduction", "Training schedule"]
        }
    
    async def _process_leave(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process leave applications."""
        employee_id = task_data.get("employee_id")
        leave_days = task_data.get("leave_days")
        
        return {
            "status": "completed",
            "employee_id": employee_id,
            "approved_days": leave_days,
            "message": "Leave processed and approved"
        }
    
    async def _schedule_review(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule performance review."""
        employee_id = task_data.get("employee_id")
        review_date = task_data.get("review_date")
        
        return {
            "status": "completed",
            "employee_id": employee_id,
            "review_date": review_date,
            "message": "Performance review scheduled"
        }
    
    async def _coordinate_training(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate training sessions."""
        training_type = task_data.get("training_type")
        participants = task_data.get("participants", [])
        
        return {
            "status": "completed",
            "training_type": training_type,
            "participants_count": len(participants),
            "message": f"Training '{training_type}' coordinated successfully"
        }
