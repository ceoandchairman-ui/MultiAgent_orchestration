"""
Customer Interface Example

Demonstrates how customers interact with the orchestration system.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from multiagent_orchestration.interfaces.customer_interface import CustomerInterface


async def main():
    """Main customer interface example."""
    
    print("=" * 60)
    print("Customer Interface Demo")
    print("=" * 60)
    print()
    
    # Create customer interface
    customer_interface = CustomerInterface(support_agent_id="support-001")
    
    # Register as guest
    print("1. Guest Registration")
    guest_result = customer_interface.register_guest(
        email="customer@example.com",
        name="Jane Smith"
    )
    print(f"   Status: {guest_result['status']}")
    print(f"   Customer ID: {guest_result['customer_id']}")
    print(f"   Session ID: {guest_result['session_id']}")
    print()
    
    # Create support ticket
    print("2. Create Support Ticket")
    ticket_result = await customer_interface.create_support_ticket(
        issue_type="Product Issue",
        description="Product not working as expected",
        priority="normal",
        contact_info={"email": "customer@example.com", "phone": "555-0123"}
    )
    print(f"   Status: {ticket_result['status']}")
    print(f"   Ticket ID: {ticket_result['ticket_id']}")
    print(f"   Expected Response: {ticket_result['expected_response']}")
    print(f"   Tracking URL: {ticket_result['tracking_url']}")
    print()
    
    # Check ticket status
    print("3. Check Ticket Status")
    status_result = await customer_interface.get_ticket_status(
        ticket_id=ticket_result['ticket_id']
    )
    print(f"   Status: {status_result['status']}")
    print(f"   Ticket Status: {status_result.get('ticket_status', 'N/A')}")
    print()
    
    # Product inquiry
    print("4. Product Inquiry")
    inquiry_result = await customer_interface.inquire_product(
        product_name="Premium Widget",
        inquiry_type="features"
    )
    print(f"   Status: {inquiry_result['status']}")
    print(f"   Product: {inquiry_result['product_name']}")
    print(f"   Information: {inquiry_result['information']}")
    print()
    
    # Check order status
    print("5. Check Order Status")
    order_result = await customer_interface.check_order_status(
        order_id="ORD-98765"
    )
    print(f"   Order ID: {order_result['order_id']}")
    print(f"   Status: {order_result['order_status']}")
    print(f"   Estimated Delivery: {order_result['estimated_delivery']}")
    print()
    
    # Submit feedback
    print("6. Submit Feedback")
    feedback_result = await customer_interface.submit_feedback(
        feedback_type="service",
        rating=5,
        comments="Excellent customer service!",
        related_ticket=ticket_result['ticket_id']
    )
    print(f"   Status: {feedback_result['status']}")
    print(f"   Feedback ID: {feedback_result['feedback_id']}")
    print()
    
    # Get FAQ answer
    print("7. Get FAQ Answer")
    faq_result = await customer_interface.get_faq_answer(
        question="How do I return a product?"
    )
    print(f"   Status: {faq_result['status']}")
    print(f"   Question: {faq_result['question']}")
    print(f"   Answer: {faq_result['answer']}")
    print()
    
    # Request callback
    print("8. Request Callback")
    callback_result = await customer_interface.request_callback(
        preferred_time="2024-01-20 14:00",
        phone_number="555-0123",
        reason="Discuss product options"
    )
    print(f"   Status: {callback_result['status']}")
    print(f"   Preferred Time: {callback_result['preferred_time']}")
    print()
    
    # Live chat
    print("9. Live Chat")
    chat_result = await customer_interface.live_chat(
        message="I need help with my recent order"
    )
    print(f"   Status: {chat_result['status']}")
    print(f"   Response: {chat_result['response']}")
    print()
    
    # View dashboard
    print("10. Customer Dashboard")
    dashboard = await customer_interface.get_dashboard()
    print(f"   Total Interactions: {dashboard['total_interactions']}")
    print(f"   Open Tickets: {dashboard['open_tickets']}")
    print(f"   Quick Actions: {', '.join(dashboard['quick_actions'])}")
    print()
    
    print("=" * 60)
    print("Customer Interface Demo Completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
