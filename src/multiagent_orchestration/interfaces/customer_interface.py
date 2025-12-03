"""
Customer Interface

Provides a unified interface for customers to interact with the multi-agent system.
"""

import uuid
from typing import Any, Dict, List, Optional
from datetime import datetime


class CustomerInterface:
    """
    Customer Interface for interacting with the orchestration system.
    
    Provides customers with seamless access to:
    - Support services
    - Product inquiries
    - Order management
    - Feedback submission
    - Account management
    """
    
    def __init__(self, support_agent_id: Optional[str] = None):
        self.support_agent_id = support_agent_id
        self.customer_id: Optional[str] = None
        self.session_id: str = str(uuid.uuid4())
        self.interaction_history: List[Dict[str, Any]] = []
        
    def authenticate(self, customer_id: str, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Authenticate a customer.
        
        Args:
            customer_id: Customer identifier
            credentials: Authentication credentials
            
        Returns:
            Authentication result
        """
        # In a real system, this would verify credentials
        self.customer_id = customer_id
        
        return {
            "status": "authenticated",
            "customer_id": customer_id,
            "session_id": self.session_id,
            "message": "Customer authenticated successfully"
        }
    
    def register_guest(self, email: str, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Register a guest customer for quick access.
        
        Args:
            email: Guest email
            name: Optional name
            
        Returns:
            Registration result
        """
        guest_id = f"GUEST-{uuid.uuid4().hex[:8]}"
        self.customer_id = guest_id
        
        return {
            "status": "registered",
            "customer_id": guest_id,
            "session_id": self.session_id,
            "message": "Guest registered successfully"
        }
    
    async def create_support_ticket(
        self,
        issue_type: str,
        description: str,
        priority: str = "normal",
        contact_info: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create a support ticket.
        
        Args:
            issue_type: Type of issue
            description: Detailed description
            priority: Priority level ('low', 'normal', 'high')
            contact_info: Contact information
            
        Returns:
            Ticket creation result
        """
        ticket_id = f"CS-TKT-{hash(description) % 10000}"
        
        interaction = {
            "ticket_id": ticket_id,
            "type": "support_ticket",
            "customer_id": self.customer_id,
            "issue_type": issue_type,
            "description": description,
            "priority": priority,
            "contact_info": contact_info or {},
            "timestamp": datetime.utcnow().isoformat(),
            "status": "open"
        }
        
        self.interaction_history.append(interaction)
        
        return {
            "status": "created",
            "ticket_id": ticket_id,
            "message": "Support ticket created successfully",
            "expected_response": "Within 24 hours",
            "tracking_url": f"/track/{ticket_id}"
        }
    
    async def get_ticket_status(self, ticket_id: str) -> Dict[str, Any]:
        """
        Get the status of a support ticket.
        
        Args:
            ticket_id: Ticket identifier
            
        Returns:
            Ticket status
        """
        # Find ticket in history
        ticket = None
        for interaction in self.interaction_history:
            if interaction.get("ticket_id") == ticket_id:
                ticket = interaction
                break
        
        if not ticket:
            return {
                "status": "not_found",
                "message": "Ticket not found"
            }
        
        return {
            "status": "found",
            "ticket_id": ticket_id,
            "ticket_status": ticket.get("status", "in_progress"),
            "created_at": ticket.get("timestamp"),
            "last_update": datetime.utcnow().isoformat(),
            "message": "Your ticket is being processed"
        }
    
    async def inquire_product(
        self,
        product_name: str,
        inquiry_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Make a product inquiry.
        
        Args:
            product_name: Name of product
            inquiry_type: Type of inquiry
            
        Returns:
            Inquiry response
        """
        inquiry_id = str(uuid.uuid4())
        
        interaction = {
            "inquiry_id": inquiry_id,
            "type": "product_inquiry",
            "customer_id": self.customer_id,
            "product_name": product_name,
            "inquiry_type": inquiry_type,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.interaction_history.append(interaction)
        
        return {
            "status": "success",
            "inquiry_id": inquiry_id,
            "product_name": product_name,
            "information": f"Product information for {product_name}",
            "message": "Inquiry processed successfully"
        }
    
    async def check_order_status(self, order_id: str) -> Dict[str, Any]:
        """
        Check order status.
        
        Args:
            order_id: Order identifier
            
        Returns:
            Order status
        """
        return {
            "status": "success",
            "order_id": order_id,
            "order_status": "processing",
            "estimated_delivery": "3-5 business days",
            "tracking_number": f"TRACK-{order_id}",
            "message": "Order is being processed"
        }
    
    async def submit_feedback(
        self,
        feedback_type: str,
        rating: int,
        comments: str,
        related_ticket: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit feedback.
        
        Args:
            feedback_type: Type of feedback
            rating: Rating (1-5)
            comments: Feedback comments
            related_ticket: Optional related ticket
            
        Returns:
            Feedback submission result
        """
        feedback_id = str(uuid.uuid4())
        
        interaction = {
            "feedback_id": feedback_id,
            "type": "feedback",
            "customer_id": self.customer_id,
            "feedback_type": feedback_type,
            "rating": rating,
            "comments": comments,
            "related_ticket": related_ticket,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.interaction_history.append(interaction)
        
        return {
            "status": "submitted",
            "feedback_id": feedback_id,
            "message": "Thank you for your feedback!"
        }
    
    async def get_faq_answer(self, question: str) -> Dict[str, Any]:
        """
        Get answer to a frequently asked question.
        
        Args:
            question: Question to ask
            
        Returns:
            FAQ answer
        """
        return {
            "status": "success",
            "question": question,
            "answer": f"FAQ answer for: {question}",
            "helpful": True,
            "related_links": [],
            "message": "Answer retrieved from knowledge base"
        }
    
    async def request_callback(
        self,
        preferred_time: str,
        phone_number: str,
        reason: str
    ) -> Dict[str, Any]:
        """
        Request a callback from support.
        
        Args:
            preferred_time: Preferred callback time
            phone_number: Contact number
            reason: Reason for callback
            
        Returns:
            Callback request result
        """
        callback_id = str(uuid.uuid4())
        
        interaction = {
            "callback_id": callback_id,
            "type": "callback_request",
            "customer_id": self.customer_id,
            "preferred_time": preferred_time,
            "phone_number": phone_number,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.interaction_history.append(interaction)
        
        return {
            "status": "scheduled",
            "callback_id": callback_id,
            "preferred_time": preferred_time,
            "message": "Callback scheduled successfully"
        }
    
    async def live_chat(self, message: str) -> Dict[str, Any]:
        """
        Send a message in live chat.
        
        Args:
            message: Chat message
            
        Returns:
            Chat response
        """
        chat_id = str(uuid.uuid4())
        
        interaction = {
            "chat_id": chat_id,
            "type": "live_chat",
            "customer_id": self.customer_id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.interaction_history.append(interaction)
        
        return {
            "status": "sent",
            "chat_id": chat_id,
            "response": "Thank you for your message. An agent will respond shortly.",
            "queue_position": 1
        }
    
    def get_interaction_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get interaction history.
        
        Args:
            limit: Maximum number of interactions to return
            
        Returns:
            List of interactions
        """
        history = self.interaction_history.copy()
        history.reverse()  # Most recent first
        
        if limit:
            history = history[:limit]
        
        return history
    
    async def get_dashboard(self) -> Dict[str, Any]:
        """
        Get customer dashboard with overview information.
        
        Returns:
            Dashboard data
        """
        return {
            "customer_id": self.customer_id,
            "session_id": self.session_id,
            "total_interactions": len(self.interaction_history),
            "recent_interactions": self.get_interaction_history(limit=5),
            "quick_actions": [
                "Create Support Ticket",
                "Check Order Status",
                "Product Inquiry",
                "Submit Feedback",
                "Live Chat"
            ],
            "open_tickets": sum(
                1 for i in self.interaction_history
                if i.get("type") == "support_ticket" and i.get("status") == "open"
            ),
            "timestamp": datetime.utcnow().isoformat()
        }
