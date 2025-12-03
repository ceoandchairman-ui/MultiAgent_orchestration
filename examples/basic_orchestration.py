"""
Basic Orchestration Example

Demonstrates the basic setup and usage of the multi-agent orchestration system.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from multiagent_orchestration.core.chief_agent import ChiefAgent
from multiagent_orchestration.agents.hr_agent import HRAgent
from multiagent_orchestration.agents.finance_agent import FinanceAgent
from multiagent_orchestration.agents.support_agent import SupportAgent
from multiagent_orchestration.agents.operations_agent import OperationsAgent


async def main():
    """Main orchestration example."""
    
    print("=" * 60)
    print("Multi-Agent Orchestration System - Basic Example")
    print("=" * 60)
    print()
    
    # Create and initialize Chief Agent
    print("1. Initializing Chief Agent...")
    chief = ChiefAgent(agent_id="chief-001")
    await chief.initialize()
    await chief.start()
    print(f"   ✓ Chief Agent started: {chief.agent_id}")
    print()
    
    # Create and initialize Slave Agents
    print("2. Initializing Slave Agents...")
    
    # HR Agent
    hr_agent = HRAgent(agent_id="hr-001")
    await hr_agent.initialize()
    await hr_agent.start()
    await hr_agent.register_with_chief(chief.agent_id)
    print(f"   ✓ HR Agent registered: {hr_agent.agent_id}")
    
    # Finance Agent
    finance_agent = FinanceAgent(agent_id="finance-001")
    await finance_agent.initialize()
    await finance_agent.start()
    await finance_agent.register_with_chief(chief.agent_id)
    print(f"   ✓ Finance Agent registered: {finance_agent.agent_id}")
    
    # Support Agent
    support_agent = SupportAgent(agent_id="support-001")
    await support_agent.initialize()
    await support_agent.start()
    await support_agent.register_with_chief(chief.agent_id)
    print(f"   ✓ Support Agent registered: {support_agent.agent_id}")
    
    # Operations Agent
    ops_agent = OperationsAgent(agent_id="ops-001")
    await ops_agent.initialize()
    await ops_agent.start()
    await ops_agent.register_with_chief(chief.agent_id)
    print(f"   ✓ Operations Agent registered: {ops_agent.agent_id}")
    print()
    
    # Wait a moment for registrations to process
    await asyncio.sleep(1)
    
    # Get system status
    print("3. System Status:")
    status = await chief.get_system_status()
    print(f"   Total Agents: {status['slave_agents']['total']}")
    print(f"   Registered Agents:")
    for agent in status['slave_agents']['registered']:
        print(f"     - {agent['agent_type']}: {agent['agent_id']}")
    print()
    
    # Assign tasks to agents
    print("4. Assigning Tasks...")
    
    # HR Task
    task1 = await chief.assign_task(
        task_id="task-001",
        task_type="onboard_employee",
        task_data={
            "employee_name": "John Doe",
            "department": "Engineering",
            "start_date": "2024-01-15"
        },
        required_capabilities=["employee_onboarding"]
    )
    print(f"   ✓ Task assigned: {task1['task_id']} -> {task1['agent_type']}")
    
    # Finance Task
    task2 = await chief.assign_task(
        task_id="task-002",
        task_type="process_invoice",
        task_data={
            "invoice_id": "INV-12345",
            "amount": 5000.00,
            "vendor": "Tech Supplies Inc."
        },
        required_capabilities=["invoice_processing"]
    )
    print(f"   ✓ Task assigned: {task2['task_id']} -> {task2['agent_type']}")
    
    # Support Task
    task3 = await chief.assign_task(
        task_id="task-003",
        task_type="resolve_ticket",
        task_data={
            "ticket_id": "TKT-9876",
            "resolution": "Issue resolved by restarting service"
        },
        required_capabilities=["ticket_management"]
    )
    print(f"   ✓ Task assigned: {task3['task_id']} -> {task3['agent_type']}")
    
    # Operations Task
    task4 = await chief.assign_task(
        task_id="task-004",
        task_type="allocate_resources",
        task_data={
            "resource_type": "compute",
            "amount": "10 instances",
            "project": "Q1 Marketing Campaign"
        },
        required_capabilities=["resource_allocation"]
    )
    print(f"   ✓ Task assigned: {task4['task_id']} -> {task4['agent_type']}")
    print()
    
    # Wait for tasks to complete
    print("5. Processing Tasks...")
    await asyncio.sleep(2)
    print("   ✓ Tasks completed")
    print()
    
    # Broadcast to all agents
    print("6. Broadcasting Status Check...")
    await chief.broadcast_to_all_agents(
        subject="status_check",
        message="Please report your current status",
        data={"requested_by": "chief"}
    )
    print("   ✓ Broadcast sent to all agents")
    print()
    
    # Final system status
    print("7. Final System Status:")
    final_status = await chief.get_system_status()
    print(f"   Active Tasks: {final_status['tasks']['active']}")
    print(f"   Completed Tasks: {final_status['tasks']['completed']}")
    print()
    
    # Cleanup
    print("8. Shutting down agents...")
    await chief.stop()
    await hr_agent.stop()
    await finance_agent.stop()
    await support_agent.stop()
    await ops_agent.stop()
    print("   ✓ All agents stopped")
    print()
    
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
