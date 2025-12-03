# Quick Start Guide

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/ceoandchairman-ui/MultiAgent_orchestration.git
cd MultiAgent_orchestration

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Basic Usage

### 1. Create a Simple Multi-Agent System

```python
import asyncio
from multiagent_orchestration.core.chief_agent import ChiefAgent
from multiagent_orchestration.agents.hr_agent import HRAgent

async def main():
    # Create and initialize Chief Agent
    chief = ChiefAgent(agent_id="chief-001")
    await chief.initialize()
    await chief.start()
    
    # Create and initialize HR Agent
    hr_agent = HRAgent(agent_id="hr-001")
    await hr_agent.initialize()
    await hr_agent.start()
    
    # Register HR agent with chief
    await chief.register_slave_agent(
        agent_id=hr_agent.agent_id,
        agent_type=hr_agent.agent_type,
        capabilities=hr_agent.capabilities
    )
    
    # Assign a task
    result = await chief.assign_task(
        task_id="task-001",
        task_type="onboard_employee",
        task_data={
            "employee_name": "John Doe",
            "department": "Engineering",
            "start_date": "2024-01-15"
        },
        required_capabilities=["employee_onboarding"]
    )
    
    print(f"Task assigned: {result}")
    
    # Clean up
    await chief.stop()
    await hr_agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Use Employee Interface

```python
import asyncio
from multiagent_orchestration.interfaces.employee_interface import EmployeeInterface

async def main():
    # Create interface
    interface = EmployeeInterface(chief_agent_id="chief-001")
    
    # Authenticate
    interface.authenticate(
        employee_id="EMP-12345",
        credentials={"username": "john.doe", "password": "****"}
    )
    
    # Submit leave request
    result = await interface.submit_leave_request(
        leave_type="vacation",
        start_date="2024-02-01",
        end_date="2024-02-05",
        reason="Family vacation"
    )
    
    print(f"Leave request: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Use Customer Interface

```python
import asyncio
from multiagent_orchestration.interfaces.customer_interface import CustomerInterface

async def main():
    # Create interface
    interface = CustomerInterface(support_agent_id="support-001")
    
    # Register as guest
    interface.register_guest(
        email="customer@example.com",
        name="Jane Smith"
    )
    
    # Create support ticket
    result = await interface.create_support_ticket(
        issue_type="Product Issue",
        description="Product not working as expected",
        priority="normal"
    )
    
    print(f"Ticket created: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Running Examples

The repository includes several complete examples:

```bash
# Basic orchestration with multiple agents
python examples/basic_orchestration.py

# Employee interface demo
python examples/employee_interface_example.py

# Customer interface demo
python examples/customer_interface_example.py
```

## Configuration

Create a `config.yaml` file to customize the system:

```yaml
system:
  name: "My Orchestration System"
  environment: "production"

agents:
  chief:
    max_concurrent_tasks: 200
  slave:
    auto_register: true

protocols:
  a2a:
    queue_size: 2000
  mcp:
    context_size: 20000

logging:
  level: "INFO"
  json_format: true
```

Load configuration in your code:

```python
from multiagent_orchestration.utils.config import Config

config = Config(config_file="config.yaml")
log_level = config.get("logging.level")
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=multiagent_orchestration

# Run specific tests
pytest tests/unit/test_agents.py
```

## Next Steps

- Read the [Architecture Documentation](ARCHITECTURE.md) for system design details
- Check the [API Reference](API.md) for complete API documentation
- Explore the examples directory for more use cases
- Customize agents for your specific departments
- Implement custom interfaces for your requirements

## Common Patterns

### Creating Custom Department Agents

```python
from multiagent_orchestration.core.slave_agent import SlaveAgent

class MarketingAgent(SlaveAgent):
    def __init__(self, agent_id=None):
        super().__init__(
            agent_id=agent_id,
            agent_type="marketing",
            department="marketing",
            capabilities=[
                "campaign_management",
                "content_creation",
                "analytics_reporting"
            ]
        )
    
    async def _execute_department_task(self, task_type, task_data):
        if task_type == "create_campaign":
            return await self._create_campaign(task_data)
        return await super()._execute_department_task(task_type, task_data)
    
    async def _create_campaign(self, task_data):
        campaign_name = task_data.get("campaign_name")
        return {
            "status": "completed",
            "campaign_name": campaign_name,
            "message": f"Campaign '{campaign_name}' created"
        }
```

### Task Assignment Pattern

```python
# Chief agent automatically selects best agent based on capabilities
result = await chief.assign_task(
    task_id="unique-task-id",
    task_type="task_name",
    task_data={"key": "value"},
    required_capabilities=["capability1", "capability2"]
)
```

### Broadcasting to All Agents

```python
await chief.broadcast_to_all_agents(
    subject="system_update",
    message="System will restart in 5 minutes",
    data={"restart_time": "14:00"}
)
```

### Monitoring System Status

```python
status = await chief.get_system_status()
print(f"Active agents: {status['slave_agents']['total']}")
print(f"Active tasks: {status['tasks']['active']}")
print(f"Completed tasks: {status['tasks']['completed']}")
```

## Troubleshooting

### Agent Not Receiving Messages

Ensure agents are started and message processing is running:

```python
await agent.start()  # This starts the message processing loop
```

### Tasks Not Being Assigned

Check that:
1. Agents are registered with the chief
2. Agents have the required capabilities
3. Agents are in READY state

```python
# Check registration
status = await chief.get_system_status()
print(status['slave_agents'])

# Check agent capabilities
agent_info = chief.slave_agents.get(agent_id)
print(agent_info['capabilities'])
```

### Import Errors

Ensure the package is installed:

```bash
pip install -e .
```

## Support

For issues or questions:
- GitHub Issues: [Create an issue](https://github.com/ceoandchairman-ui/MultiAgent_orchestration/issues)
- Documentation: Check the `docs/` directory
- Examples: Review the `examples/` directory
