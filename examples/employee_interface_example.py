"""
Employee Interface Example

Demonstrates how employees interact with the orchestration system.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from multiagent_orchestration.interfaces.employee_interface import EmployeeInterface


async def main():
    """Main employee interface example."""
    
    print("=" * 60)
    print("Employee Interface Demo")
    print("=" * 60)
    print()
    
    # Create employee interface
    employee_interface = EmployeeInterface(chief_agent_id="chief-001")
    
    # Authenticate
    print("1. Employee Authentication")
    auth_result = employee_interface.authenticate(
        employee_id="EMP-12345",
        credentials={"username": "john.doe", "password": "****"}
    )
    print(f"   Status: {auth_result['status']}")
    print(f"   Employee ID: {auth_result['employee_id']}")
    print(f"   Session ID: {auth_result['session_id']}")
    print()
    
    # Submit leave request
    print("2. Submit Leave Request")
    leave_result = await employee_interface.submit_leave_request(
        leave_type="vacation",
        start_date="2024-02-01",
        end_date="2024-02-05",
        reason="Family vacation"
    )
    print(f"   Status: {leave_result['status']}")
    print(f"   Request ID: {leave_result['request_id']}")
    print(f"   Expected Response: {leave_result['expected_response']}")
    print()
    
    # Create support ticket
    print("3. Create Support Ticket")
    ticket_result = await employee_interface.create_support_ticket(
        issue_type="IT Support",
        description="Laptop not connecting to VPN",
        priority="high"
    )
    print(f"   Status: {ticket_result['status']}")
    print(f"   Ticket ID: {ticket_result['ticket_id']}")
    print()
    
    # Query policy
    print("4. Query Company Policy")
    policy_result = await employee_interface.query_policy(
        policy_category="remote_work"
    )
    print(f"   Status: {policy_result['status']}")
    print(f"   Category: {policy_result['policy_category']}")
    print(f"   Information: {policy_result['information']}")
    print()
    
    # Submit expense
    print("5. Submit Expense")
    expense_result = await employee_interface.submit_expense(
        amount=125.50,
        category="Travel",
        description="Client meeting lunch",
        receipt_url="https://example.com/receipt.pdf"
    )
    print(f"   Status: {expense_result['status']}")
    print(f"   Expense ID: {expense_result['expense_id']}")
    print(f"   Amount: ${expense_result['amount']}")
    print()
    
    # Request training
    print("6. Request Training")
    training_result = await employee_interface.request_training(
        training_type="Leadership Development",
        preferred_dates=["2024-03-15", "2024-03-20"]
    )
    print(f"   Status: {training_result['status']}")
    print(f"   Training Type: {training_result['training_type']}")
    print()
    
    # View dashboard
    print("7. Employee Dashboard")
    dashboard = await employee_interface.get_dashboard()
    print(f"   Total Requests: {dashboard['total_requests']}")
    print(f"   Quick Actions: {', '.join(dashboard['quick_actions'])}")
    print()
    
    # View request history
    print("8. Request History")
    history = employee_interface.get_request_history(limit=3)
    print(f"   Recent Requests: {len(history)}")
    for i, request in enumerate(history, 1):
        req_type = request.get('request_type', 'unknown')
        print(f"     {i}. {req_type}")
    print()
    
    print("=" * 60)
    print("Employee Interface Demo Completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
