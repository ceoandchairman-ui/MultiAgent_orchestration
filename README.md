# Multi-Agent Orchestration System

A comprehensive multi-agent orchestration system designed for automation of organizational operations. This system features MCP (Model Context Protocol) powered agents with A2A (Agent-to-Agent) protocol for seamless communication, providing coordinated task management across departments with dedicated interfaces for employees and customers.

## 🌟 Features

### Core Architecture
- **Chief Agent**: Master orchestrator that coordinates all slave agents, manages task distribution, and maintains system health
- **Slave Agents**: Specialized agents for different departments (HR, Finance, Support, Operations)
- **MCP Protocol**: Model Context Protocol for managing agent context, state, and interactions
- **A2A Protocol**: Agent-to-Agent communication protocol for reliable message passing

### Department Agents
- **HR Agent**: Employee onboarding, leave management, performance reviews, policy queries
- **Finance Agent**: Invoice processing, expense approvals, payment processing, financial reporting
- **Support Agent**: Ticket management, issue resolution, FAQ responses, customer assistance
- **Operations Agent**: Resource allocation, workflow automation, process optimization, system monitoring

### User Interfaces
- **Employee Interface**: Seamless access to HR services, support requests, expense submission, and training
- **Customer Interface**: Support tickets, product inquiries, order tracking, feedback submission, live chat

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ceoandchairman-ui/MultiAgent_orchestration.git
cd MultiAgent_orchestration

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Basic Usage

```python
import asyncio
from multiagent_orchestration.core.chief_agent import ChiefAgent
from multiagent_orchestration.agents.hr_agent import HRAgent

async def main():
    # Create and initialize Chief Agent
    chief = ChiefAgent(agent_id="chief-001")
    await chief.initialize()
    await chief.start()
    
    # Create and register HR Agent
    hr_agent = HRAgent(agent_id="hr-001")
    await hr_agent.initialize()
    await hr_agent.start()
    await hr_agent.register_with_chief(chief.agent_id)
    
    # Assign a task
    result = await chief.assign_task(
        task_id="task-001",
        task_type="onboard_employee",
        task_data={
            "employee_name": "John Doe",
            "department": "Engineering"
        },
        required_capabilities=["employee_onboarding"]
    )
    
    print(f"Task assigned: {result}")

asyncio.run(main())
```

## 📚 Documentation

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Chief Agent (MCP)                       │
│                  (Task Orchestrator)                        │
└────────┬────────────────────────────────┬───────────────────┘
         │                                │
         │        A2A Protocol            │
         │                                │
    ┌────▼─────┐    ┌──────────┐    ┌────▼────┐    ┌─────────┐
    │ HR Agent │    │ Finance  │    │ Support │    │   Ops   │
    │  (MCP)   │    │  Agent   │    │  Agent  │    │  Agent  │
    │          │    │  (MCP)   │    │  (MCP)  │    │  (MCP)  │
    └────┬─────┘    └────┬─────┘    └────┬────┘    └────┬────┘
         │               │               │              │
         └───────────────┴───────────────┴──────────────┘
                              │
              ┌───────────────┴────────────────┐
              │                                │
         ┌────▼────────┐              ┌────────▼──────┐
         │  Employee   │              │   Customer    │
         │  Interface  │              │   Interface   │
         └─────────────┘              └───────────────┘
```

### Protocols

#### MCP (Model Context Protocol)
The MCP protocol manages agent context, state, and model interactions:
- Agent initialization and capability registration
- Context updates and queries
- Task execution tracking
- Status monitoring
- History management

#### A2A (Agent-to-Agent Protocol)
The A2A protocol enables reliable communication between agents:
- Message types: REQUEST, RESPONSE, BROADCAST, TASK_ASSIGNMENT, STATUS_UPDATE
- Priority levels: LOW, NORMAL, HIGH, CRITICAL
- Message queuing and routing
- Handler registration
- Message history tracking

### Examples

Check the `examples/` directory for complete examples:

1. **basic_orchestration.py**: Complete setup with chief and multiple slave agents
2. **employee_interface_example.py**: Employee interaction demonstrations
3. **customer_interface_example.py**: Customer interaction demonstrations

Run examples:
```bash
python examples/basic_orchestration.py
python examples/employee_interface_example.py
python examples/customer_interface_example.py
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=multiagent_orchestration

# Run specific test file
pytest tests/unit/test_chief_agent.py
```

## 📋 Configuration

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
    timeout: 60
  mcp:
    context_size: 20000
    history_size: 200

interfaces:
  employee:
    session_timeout: 7200
  customer:
    guest_access: true
    session_timeout: 3600

logging:
  level: "INFO"
  json_format: true
```

## 🔧 Development

### Project Structure

```
MultiAgent_orchestration/
├── src/
│   └── multiagent_orchestration/
│       ├── core/              # Core agent implementations
│       │   ├── base_agent.py
│       │   ├── chief_agent.py
│       │   ├── slave_agent.py
│       │   └── agent_registry.py
│       ├── agents/            # Department-specific agents
│       │   ├── hr_agent.py
│       │   ├── finance_agent.py
│       │   ├── support_agent.py
│       │   └── operations_agent.py
│       ├── protocols/         # Communication protocols
│       │   ├── a2a_protocol.py
│       │   └── mcp_protocol.py
│       ├── interfaces/        # User interfaces
│       │   ├── employee_interface.py
│       │   └── customer_interface.py
│       └── utils/             # Utilities
│           ├── logger.py
│           └── config.py
├── examples/                  # Usage examples
├── tests/                     # Test suite
├── config/                    # Configuration files
└── docs/                      # Additional documentation
```

### Code Style

This project uses:
- **black** for code formatting
- **flake8** for linting
- **mypy** for type checking

```bash
# Format code
black src/

# Lint
flake8 src/

# Type check
mypy src/
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Use Cases

### Organizational Automation
- Automated employee onboarding workflows
- Expense approval and processing
- IT support ticket routing
- Resource allocation and optimization

### Customer Support
- Multi-channel customer support
- Automated ticket assignment
- FAQ and knowledge base queries
- Feedback collection and analysis

### Inter-Department Coordination
- Seamless task delegation between departments
- Real-time status updates
- Centralized monitoring and reporting
- Escalation handling

## 📞 Support

For issues, questions, or contributions:
- GitHub Issues: [Create an issue](https://github.com/ceoandchairman-ui/MultiAgent_orchestration/issues)
- Documentation: [Check the docs](./docs/)

## 🙏 Acknowledgments

Built with modern Python async/await patterns and designed for scalability and reliability in enterprise environments.