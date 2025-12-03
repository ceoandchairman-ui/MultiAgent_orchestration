"""Unit tests for agent implementations."""

import pytest
import asyncio

from multiagent_orchestration.core.chief_agent import ChiefAgent
from multiagent_orchestration.agents.hr_agent import HRAgent
from multiagent_orchestration.agents.finance_agent import FinanceAgent


class TestChiefAgent:
    """Test Chief Agent functionality."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test chief agent initialization."""
        chief = ChiefAgent(agent_id="chief-test")
        await chief.initialize()
        
        assert chief.agent_id == "chief-test"
        assert chief.agent_type == "chief"
        assert chief.is_initialized is True
        assert "task_orchestration" in chief.capabilities
    
    @pytest.mark.asyncio
    async def test_register_slave_agent(self):
        """Test registering a slave agent."""
        chief = ChiefAgent(agent_id="chief-test")
        await chief.initialize()
        
        result = await chief.register_slave_agent(
            agent_id="slave-1",
            agent_type="hr",
            capabilities=["employee_onboarding"]
        )
        
        assert result["status"] == "success"
        assert "slave-1" in chief.slave_agents
        assert chief.slave_agents["slave-1"]["agent_type"] == "hr"
    
    @pytest.mark.asyncio
    async def test_assign_task(self):
        """Test task assignment."""
        chief = ChiefAgent(agent_id="chief-test")
        await chief.initialize()
        await chief.start()
        
        # Register an agent
        await chief.register_slave_agent(
            agent_id="hr-1",
            agent_type="hr",
            capabilities=["employee_onboarding"]
        )
        
        # Assign a task
        result = await chief.assign_task(
            task_id="task-1",
            task_type="onboard_employee",
            task_data={"employee_name": "John Doe"},
            required_capabilities=["employee_onboarding"]
        )
        
        assert result["status"] == "success"
        assert result["assigned_to"] == "hr-1"
        assert "task-1" in chief.active_assignments
        
        await chief.stop()
    
    @pytest.mark.asyncio
    async def test_get_system_status(self):
        """Test getting system status."""
        chief = ChiefAgent(agent_id="chief-test")
        await chief.initialize()
        
        # Register some agents
        await chief.register_slave_agent("agent-1", "hr", ["test"])
        await chief.register_slave_agent("agent-2", "finance", ["test"])
        
        status = await chief.get_system_status()
        
        assert status["slave_agents"]["total"] == 2
        assert status["tasks"]["total_assigned"] == 0


class TestHRAgent:
    """Test HR Agent functionality."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test HR agent initialization."""
        hr_agent = HRAgent(agent_id="hr-test")
        await hr_agent.initialize()
        
        assert hr_agent.agent_id == "hr-test"
        assert hr_agent.agent_type == "hr"
        assert hr_agent.department == "hr"
        assert "employee_onboarding" in hr_agent.capabilities
    
    @pytest.mark.asyncio
    async def test_onboard_employee_task(self):
        """Test employee onboarding task."""
        hr_agent = HRAgent(agent_id="hr-test")
        await hr_agent.initialize()
        
        result = await hr_agent.execute_task({
            "task_id": "task-1",
            "task_type": "onboard_employee",
            "employee_name": "Jane Doe",
            "department": "Engineering"
        })
        
        assert result["status"] == "completed"
        assert result["employee_name"] == "Jane Doe"
        assert "next_steps" in result
    
    @pytest.mark.asyncio
    async def test_process_leave_task(self):
        """Test leave processing task."""
        hr_agent = HRAgent(agent_id="hr-test")
        await hr_agent.initialize()
        
        result = await hr_agent.execute_task({
            "task_id": "task-2",
            "task_type": "process_leave",
            "employee_id": "EMP-123",
            "leave_days": 5
        })
        
        assert result["status"] == "completed"
        assert result["employee_id"] == "EMP-123"
        assert result["approved_days"] == 5


class TestFinanceAgent:
    """Test Finance Agent functionality."""
    
    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test finance agent initialization."""
        finance_agent = FinanceAgent(agent_id="finance-test")
        await finance_agent.initialize()
        
        assert finance_agent.agent_id == "finance-test"
        assert finance_agent.agent_type == "finance"
        assert finance_agent.department == "finance"
        assert "invoice_processing" in finance_agent.capabilities
    
    @pytest.mark.asyncio
    async def test_process_invoice_task(self):
        """Test invoice processing task."""
        finance_agent = FinanceAgent(agent_id="finance-test")
        await finance_agent.initialize()
        
        result = await finance_agent.execute_task({
            "task_id": "task-1",
            "task_type": "process_invoice",
            "invoice_id": "INV-123",
            "amount": 1000.00,
            "vendor": "Test Vendor"
        })
        
        assert result["status"] == "completed"
        assert result["invoice_id"] == "INV-123"
        assert result["amount"] == 1000.00
    
    @pytest.mark.asyncio
    async def test_approve_expense_task(self):
        """Test expense approval task."""
        finance_agent = FinanceAgent(agent_id="finance-test")
        await finance_agent.initialize()
        
        result = await finance_agent.execute_task({
            "task_id": "task-2",
            "task_type": "approve_expense",
            "expense_id": "EXP-456",
            "amount": 250.00,
            "category": "Travel"
        })
        
        assert result["status"] == "completed"
        assert result["approved"] is True
        assert result["expense_id"] == "EXP-456"
