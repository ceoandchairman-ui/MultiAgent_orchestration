# API Reference

## Core Classes

### ChiefAgent

The master orchestrator that coordinates all slave agents.

```python
from multiagent_orchestration.core.chief_agent import ChiefAgent

# Create chief agent
chief = ChiefAgent(agent_id="chief-001")

# Initialize and start
await chief.initialize()
await chief.start()

# Register slave agents
await chief.register_slave_agent(
    agent_id="agent-1",
    agent_type="hr",
    capabilities=["employee_onboarding"]
)

# Assign tasks
result = await chief.assign_task(
    task_id="task-1",
    task_type="onboard_employee",
    task_data={"employee_name": "John Doe"},
    required_capabilities=["employee_onboarding"]
)

# Get system status
status = await chief.get_system_status()

# Broadcast to all agents
await chief.broadcast_to_all_agents(
    subject="announcement",
    message="System update",
    data={}
)

# Stop agent
await chief.stop()
```

### SlaveAgent / Department Agents

Specialized agents for different departments.

```python
from multiagent_orchestration.agents.hr_agent import HRAgent
from multiagent_orchestration.agents.finance_agent import FinanceAgent
from multiagent_orchestration.agents.support_agent import SupportAgent
from multiagent_orchestration.agents.operations_agent import OperationsAgent

# Create and initialize HR agent
hr_agent = HRAgent(agent_id="hr-001")
await hr_agent.initialize()
await hr_agent.start()

# Register with chief
await chief.register_slave_agent(
    agent_id=hr_agent.agent_id,
    agent_type=hr_agent.agent_type,
    capabilities=hr_agent.capabilities
)

# Get agent status
status = await hr_agent.get_status()
```

## Protocols

### A2A Protocol

Agent-to-agent communication protocol.

```python
from multiagent_orchestration.protocols.a2a_protocol import (
    A2AProtocol,
    MessageType,
    MessagePriority
)

# Create protocol instance
protocol = A2AProtocol()

# Register message handler
async def handle_request(message):
    print(f"Received: {message.payload}")

protocol.register_handler(MessageType.REQUEST, handle_request)

# Send message
message = await protocol.send_message(
    sender_id="agent-1",
    recipient_id="agent-2",
    message_type=MessageType.REQUEST,
    payload={"data": "value"},
    priority=MessagePriority.NORMAL
)

# Start processing messages
asyncio.create_task(protocol.process_messages())

# Get message history
history = protocol.get_message_history(limit=10)
```

### MCP Protocol

Model Context Protocol for agent state management.

```python
from multiagent_orchestration.protocols.mcp_protocol import (
    MCPProtocol,
    MCPAction
)

# Create protocol instance
protocol = MCPProtocol(agent_id="agent-1", agent_type="hr")

# Initialize agent
await protocol.initialize(
    capabilities=["employee_onboarding"],
    metadata={"department": "hr"}
)

# Update context
await protocol.update_context({
    "state": {"current_load": "high"},
    "metadata": {"last_update": "2024-01-01"}
})

# Execute task
await protocol.execute_task(
    task_id="task-1",
    task_type="onboard_employee",
    task_data={"employee_name": "John Doe"}
)

# Complete task
await protocol.complete_task("task-1", {"status": "success"})

# Get status
status = await protocol.get_status()

# Get context
context = protocol.get_context()
```

## Interfaces

### Employee Interface

Interface for employee interactions.

```python
from multiagent_orchestration.interfaces.employee_interface import EmployeeInterface

# Create interface
interface = EmployeeInterface(chief_agent_id="chief-001")

# Authenticate
auth = interface.authenticate(
    employee_id="EMP-123",
    credentials={"username": "user", "password": "pass"}
)

# Submit leave request
result = await interface.submit_leave_request(
    leave_type="vacation",
    start_date="2024-02-01",
    end_date="2024-02-05",
    reason="Family vacation"
)

# Create support ticket
ticket = await interface.create_support_ticket(
    issue_type="IT Support",
    description="Issue description",
    priority="high"
)

# Query policy
policy = await interface.query_policy(
    policy_category="remote_work"
)

# Submit expense
expense = await interface.submit_expense(
    amount=125.50,
    category="Travel",
    description="Client meeting"
)

# Request training
training = await interface.request_training(
    training_type="Leadership",
    preferred_dates=["2024-03-01"]
)

# Get dashboard
dashboard = await interface.get_dashboard()

# Get request history
history = interface.get_request_history(limit=10)
```

### Customer Interface

Interface for customer interactions.

```python
from multiagent_orchestration.interfaces.customer_interface import CustomerInterface

# Create interface
interface = CustomerInterface(support_agent_id="support-001")

# Register guest
guest = interface.register_guest(
    email="customer@example.com",
    name="John Doe"
)

# Or authenticate
auth = interface.authenticate(
    customer_id="CUST-123",
    credentials={"username": "user", "password": "pass"}
)

# Create support ticket
ticket = await interface.create_support_ticket(
    issue_type="Product Issue",
    description="Issue description",
    priority="normal"
)

# Get ticket status
status = await interface.get_ticket_status(ticket_id="TKT-123")

# Product inquiry
inquiry = await interface.inquire_product(
    product_name="Product Name",
    inquiry_type="features"
)

# Check order status
order = await interface.check_order_status(order_id="ORD-123")

# Submit feedback
feedback = await interface.submit_feedback(
    feedback_type="service",
    rating=5,
    comments="Great service!"
)

# Get FAQ answer
faq = await interface.get_faq_answer(
    question="How do I return a product?"
)

# Request callback
callback = await interface.request_callback(
    preferred_time="2024-01-20 14:00",
    phone_number="555-0123",
    reason="Product inquiry"
)

# Live chat
chat = await interface.live_chat(
    message="I need help"
)

# Get dashboard
dashboard = await interface.get_dashboard()
```

## Utilities

### Configuration

```python
from multiagent_orchestration.utils.config import Config

# Load configuration
config = Config(config_file="config.yaml")

# Get values
value = config.get("system.name", default="Default Name")
log_level = config.get("logging.level")

# Set values
config.set("system.environment", "production")

# Get all config
all_config = config.to_dict()
```

### Logging

```python
from multiagent_orchestration.utils.logger import setup_logger

# Setup logger
logger = setup_logger(
    name="my_agent",
    level=logging.INFO,
    json_format=True
)

# Use logger
logger.info("Agent started")
logger.error("Error occurred", extra={"agent_id": "agent-1"})
```

## Message Types

### A2A Message Types

- `REQUEST`: Request for action or information
- `RESPONSE`: Response to a request
- `BROADCAST`: Message to all agents
- `NOTIFICATION`: One-way notification
- `TASK_ASSIGNMENT`: Task assignment from chief
- `TASK_COMPLETION`: Task completion notification
- `STATUS_UPDATE`: Status update notification
- `ERROR`: Error notification

### Message Priorities

- `LOW`: Low priority, process when idle
- `NORMAL`: Normal priority (default)
- `HIGH`: High priority, process soon
- `CRITICAL`: Critical priority, process immediately

## MCP Actions

- `INITIALIZE`: Initialize agent with capabilities
- `UPDATE_CONTEXT`: Update agent context data
- `QUERY_CONTEXT`: Query current context state
- `EXECUTE_TASK`: Start task execution
- `GET_STATUS`: Retrieve agent status
- `RESET`: Reset agent to initial state
- `TERMINATE`: Shutdown agent

## MCP Status States

- `IDLE`: Agent is idle and ready
- `INITIALIZING`: Agent is being initialized
- `READY`: Agent is ready for tasks
- `PROCESSING`: Agent is executing a task
- `WAITING`: Agent is waiting for resources
- `ERROR`: Agent encountered an error
- `TERMINATED`: Agent has been terminated

## Agent Registry

```python
from multiagent_orchestration.core.agent_registry import AgentRegistry

# Create registry
registry = AgentRegistry()

# Register agent
result = registry.register_agent(
    agent_id="agent-1",
    agent_type="hr",
    capabilities=["employee_onboarding"],
    metadata={"department": "hr"}
)

# Get agent
agent_info = registry.get_agent("agent-1")

# Get agents by type
hr_agents = registry.get_agents_by_type("hr")

# Get agents by department
dept_agents = registry.get_agents_by_department("hr")

# Get agents by capability
capable_agents = registry.get_agents_by_capability("employee_onboarding")

# Get all agents
all_agents = registry.get_all_agents()

# Get registry stats
stats = registry.get_registry_stats()

# Unregister agent
result = registry.unregister_agent("agent-1")
```

## Error Handling

All async methods can raise exceptions. Always wrap them in try-except blocks:

```python
try:
    result = await chief.assign_task(
        task_id="task-1",
        task_type="test",
        task_data={},
        required_capabilities=["test_capability"]
    )
except Exception as e:
    logger.error(f"Task assignment failed: {e}")
```

## Best Practices

1. **Always initialize agents before starting them**
   ```python
   await agent.initialize()
   await agent.start()
   ```

2. **Use appropriate message priorities**
   ```python
   # For critical tasks
   priority=MessagePriority.CRITICAL
   
   # For normal operations
   priority=MessagePriority.NORMAL
   ```

3. **Handle errors gracefully**
   ```python
   try:
       result = await operation()
   except Exception as e:
       logger.error(f"Operation failed: {e}")
   ```

4. **Clean up resources**
   ```python
   await agent.stop()
   ```

5. **Use context managers when possible**
   ```python
   async with agent:
       # Agent is started automatically
       await agent.process_task()
   # Agent is stopped automatically
   ```
