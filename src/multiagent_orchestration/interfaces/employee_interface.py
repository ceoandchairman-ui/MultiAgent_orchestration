"""
Employee Interface

Provides a unified interface for employees to interact with the multi-agent system.
"""

import uuid
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..protocols.a2a_protocol import MessageType, MessagePriority


class EmployeeInterface:
    """
    Employee Interface for interacting with the orchestration system.
    
    Provides employees with seamless access to:
    - HR services
    - Support requests
    - Task management
    - Resource requests
    - Information queries
    """
    
    def __init__(self, chief_agent_id: str):
        self.chief_agent_id = chief_agent_id
        self.employee_id: Optional[str] = None
        self.session_id: str = str(uuid.uuid4())
        self.request_history: List[Dict[str, Any]] = []
        
    def authenticate(self, employee_id: str, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Authenticate an employee.
        
        Args:
            employee_id: Employee identifier
            credentials: Authentication credentials
            
        Returns:
            Authentication result
        """
        # In a real system, this would verify credentials
        self.employee_id = employee_id
        
        return {
            "status": "authenticated",
            "employee_id": employee_id,
            "session_id": self.session_id,
            "message": "Employee authenticated successfully"
        }
    
    async def submit_leave_request(
        self,
        leave_type: str,
        start_date: str,
        end_date: str,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit a leave request.
        
        Args:
            leave_type: Type of leave (e.g., 'vacation', 'sick')
            start_date: Leave start date
            end_date: Leave end date
            reason: Optional reason for leave
            
        Returns:
            Request result
        """
        request_id = str(uuid.uuid4())
        
        request = {
            "request_id": request_id,
            "request_type": "leave_request",
            "employee_id": self.employee_id,
            "leave_type": leave_type,
            "dates": {"start": start_date, "end": end_date},
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.request_history.append(request)
        
        return {
            "status": "submitted",
            "request_id": request_id,
            "message": "Leave request submitted successfully",
            "expected_response": "24 hours"
        }
    
    async def create_support_ticket(
        self,
        issue_type: str,
        description: str,
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """
        Create a support ticket.
        
        Args:
            issue_type: Type of issue
            description: Detailed description
            priority: Priority level ('low', 'normal', 'high')
            
        Returns:
            Ticket creation result
        """
        ticket_id = f"TKT-{hash(description) % 10000}"
        
        request = {
            "ticket_id": ticket_id,
            "request_type": "create_ticket",
            "employee_id": self.employee_id,
            "issue_type": issue_type,
            "description": description,
            "priority": priority,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.request_history.append(request)
        
        return {
            "status": "created",
            "ticket_id": ticket_id,
            "message": "Support ticket created successfully",
            "expected_response": "Based on priority"
        }
    
    async def query_policy(self, policy_category: str) -> Dict[str, Any]:
        """
        Query company policies.
        
        Args:
            policy_category: Category of policy to query
            
        Returns:
            Policy information
        """
        request_id = str(uuid.uuid4())
        
        request = {
            "request_id": request_id,
            "request_type": "policy_query",
            "employee_id": self.employee_id,
            "policy_category": policy_category,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.request_history.append(request)
        
        return {
            "status": "success",
            "policy_category": policy_category,
            "information": f"Policy information for {policy_category}",
            "details": "Detailed policy information would be provided here"
        }
    
    async def submit_expense(
        self,
        amount: float,
        category: str,
        description: str,
        receipt_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit an expense for approval.
        
        Args:
            amount: Expense amount
            category: Expense category
            description: Description of expense
            receipt_url: Optional receipt URL
            
        Returns:
            Submission result
        """
        expense_id = f"EXP-{uuid.uuid4().hex[:8]}"
        
        request = {
            "expense_id": expense_id,
            "request_type": "submit_expense",
            "employee_id": self.employee_id,
            "amount": amount,
            "category": category,
            "description": description,
            "receipt_url": receipt_url,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.request_history.append(request)
        
        return {
            "status": "submitted",
            "expense_id": expense_id,
            "amount": amount,
            "message": "Expense submitted for approval",
            "expected_approval": "2-3 business days"
        }
    
    async def request_training(
        self,
        training_type: str,
        preferred_dates: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Request training enrollment.
        
        Args:
            training_type: Type of training
            preferred_dates: Optional preferred dates
            
        Returns:
            Request result
        """
        request_id = str(uuid.uuid4())
        
        request = {
            "request_id": request_id,
            "request_type": "training_request",
            "employee_id": self.employee_id,
            "training_type": training_type,
            "preferred_dates": preferred_dates,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.request_history.append(request)
        
        return {
            "status": "requested",
            "request_id": request_id,
            "training_type": training_type,
            "message": "Training request submitted successfully"
        }
    
    async def get_request_status(self, request_id: str) -> Dict[str, Any]:
        """
        Get the status of a previous request.
        
        Args:
            request_id: Request identifier
            
        Returns:
            Request status
        """
        # Find request in history
        request = None
        for req in self.request_history:
            if req.get("request_id") == request_id or req.get("ticket_id") == request_id:
                request = req
                break
        
        if not request:
            return {
                "status": "not_found",
                "message": "Request not found"
            }
        
        return {
            "status": "found",
            "request": request,
            "current_status": "in_progress",
            "message": "Request is being processed"
        }
    
    def get_request_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get request history.
        
        Args:
            limit: Maximum number of requests to return
            
        Returns:
            List of requests
        """
        history = self.request_history.copy()
        history.reverse()  # Most recent first
        
        if limit:
            history = history[:limit]
        
        return history
    
    async def get_dashboard(self) -> Dict[str, Any]:
        """
        Get employee dashboard with overview information.
        
        Returns:
            Dashboard data
        """
        return {
            "employee_id": self.employee_id,
            "session_id": self.session_id,
            "total_requests": len(self.request_history),
            "recent_requests": self.get_request_history(limit=5),
            "quick_actions": [
                "Submit Leave Request",
                "Create Support Ticket",
                "Submit Expense",
                "Query Policy"
            ],
            "notifications": [],
            "timestamp": datetime.utcnow().isoformat()
        }
