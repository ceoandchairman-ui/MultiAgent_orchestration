"""Unit tests for user interfaces."""

import pytest

from multiagent_orchestration.interfaces.employee_interface import EmployeeInterface
from multiagent_orchestration.interfaces.customer_interface import CustomerInterface


class TestEmployeeInterface:
    """Test Employee Interface functionality."""
    
    def test_authentication(self):
        """Test employee authentication."""
        interface = EmployeeInterface(chief_agent_id="chief-1")
        
        result = interface.authenticate(
            employee_id="EMP-123",
            credentials={"username": "test", "password": "test"}
        )
        
        assert result["status"] == "authenticated"
        assert result["employee_id"] == "EMP-123"
        assert interface.employee_id == "EMP-123"
    
    @pytest.mark.asyncio
    async def test_submit_leave_request(self):
        """Test submitting a leave request."""
        interface = EmployeeInterface(chief_agent_id="chief-1")
        interface.authenticate("EMP-123", {})
        
        result = await interface.submit_leave_request(
            leave_type="vacation",
            start_date="2024-01-01",
            end_date="2024-01-05",
            reason="Holiday"
        )
        
        assert result["status"] == "submitted"
        assert "request_id" in result
        assert len(interface.request_history) == 1
    
    @pytest.mark.asyncio
    async def test_create_support_ticket(self):
        """Test creating a support ticket."""
        interface = EmployeeInterface(chief_agent_id="chief-1")
        interface.authenticate("EMP-123", {})
        
        result = await interface.create_support_ticket(
            issue_type="IT Support",
            description="Computer issue",
            priority="high"
        )
        
        assert result["status"] == "created"
        assert "ticket_id" in result
    
    @pytest.mark.asyncio
    async def test_submit_expense(self):
        """Test submitting an expense."""
        interface = EmployeeInterface(chief_agent_id="chief-1")
        interface.authenticate("EMP-123", {})
        
        result = await interface.submit_expense(
            amount=100.00,
            category="Travel",
            description="Client meeting"
        )
        
        assert result["status"] == "submitted"
        assert result["amount"] == 100.00
        assert "expense_id" in result
    
    @pytest.mark.asyncio
    async def test_request_training(self):
        """Test requesting training."""
        interface = EmployeeInterface(chief_agent_id="chief-1")
        interface.authenticate("EMP-123", {})
        
        result = await interface.request_training(
            training_type="Leadership",
            preferred_dates=["2024-03-01"]
        )
        
        assert result["status"] == "requested"
        assert result["training_type"] == "Leadership"
    
    def test_request_history(self):
        """Test getting request history."""
        interface = EmployeeInterface(chief_agent_id="chief-1")
        interface.authenticate("EMP-123", {})
        
        # Add some requests
        interface.request_history = [
            {"request_id": "1", "type": "leave"},
            {"request_id": "2", "type": "ticket"},
            {"request_id": "3", "type": "expense"}
        ]
        
        history = interface.get_request_history(limit=2)
        assert len(history) == 2
    
    @pytest.mark.asyncio
    async def test_get_dashboard(self):
        """Test getting employee dashboard."""
        interface = EmployeeInterface(chief_agent_id="chief-1")
        interface.authenticate("EMP-123", {})
        
        dashboard = await interface.get_dashboard()
        
        assert dashboard["employee_id"] == "EMP-123"
        assert "quick_actions" in dashboard
        assert "recent_requests" in dashboard


class TestCustomerInterface:
    """Test Customer Interface functionality."""
    
    def test_authentication(self):
        """Test customer authentication."""
        interface = CustomerInterface(support_agent_id="support-1")
        
        result = interface.authenticate(
            customer_id="CUST-123",
            credentials={"username": "test", "password": "test"}
        )
        
        assert result["status"] == "authenticated"
        assert result["customer_id"] == "CUST-123"
        assert interface.customer_id == "CUST-123"
    
    def test_guest_registration(self):
        """Test guest registration."""
        interface = CustomerInterface(support_agent_id="support-1")
        
        result = interface.register_guest(
            email="guest@example.com",
            name="Guest User"
        )
        
        assert result["status"] == "registered"
        assert "GUEST-" in result["customer_id"]
    
    @pytest.mark.asyncio
    async def test_create_support_ticket(self):
        """Test creating a support ticket."""
        interface = CustomerInterface(support_agent_id="support-1")
        interface.register_guest("test@example.com")
        
        result = await interface.create_support_ticket(
            issue_type="Product Issue",
            description="Not working",
            priority="normal"
        )
        
        assert result["status"] == "created"
        assert "ticket_id" in result
        assert "tracking_url" in result
    
    @pytest.mark.asyncio
    async def test_inquire_product(self):
        """Test product inquiry."""
        interface = CustomerInterface(support_agent_id="support-1")
        interface.register_guest("test@example.com")
        
        result = await interface.inquire_product(
            product_name="Test Product",
            inquiry_type="features"
        )
        
        assert result["status"] == "success"
        assert result["product_name"] == "Test Product"
    
    @pytest.mark.asyncio
    async def test_check_order_status(self):
        """Test checking order status."""
        interface = CustomerInterface(support_agent_id="support-1")
        interface.register_guest("test@example.com")
        
        result = await interface.check_order_status(order_id="ORD-123")
        
        assert result["status"] == "success"
        assert result["order_id"] == "ORD-123"
    
    @pytest.mark.asyncio
    async def test_submit_feedback(self):
        """Test submitting feedback."""
        interface = CustomerInterface(support_agent_id="support-1")
        interface.register_guest("test@example.com")
        
        result = await interface.submit_feedback(
            feedback_type="service",
            rating=5,
            comments="Great service"
        )
        
        assert result["status"] == "submitted"
        assert "feedback_id" in result
    
    @pytest.mark.asyncio
    async def test_request_callback(self):
        """Test requesting a callback."""
        interface = CustomerInterface(support_agent_id="support-1")
        interface.register_guest("test@example.com")
        
        result = await interface.request_callback(
            preferred_time="2024-01-20 14:00",
            phone_number="555-0123",
            reason="Product inquiry"
        )
        
        assert result["status"] == "scheduled"
    
    @pytest.mark.asyncio
    async def test_get_dashboard(self):
        """Test getting customer dashboard."""
        interface = CustomerInterface(support_agent_id="support-1")
        interface.register_guest("test@example.com")
        
        dashboard = await interface.get_dashboard()
        
        assert "customer_id" in dashboard
        assert "quick_actions" in dashboard
        assert "open_tickets" in dashboard
