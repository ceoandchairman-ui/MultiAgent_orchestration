"""
Multi-Agent Orchestration System

A comprehensive system for orchestrating multiple AI agents using MCP (Model Context Protocol)
and A2A (Agent-to-Agent) communication protocol for organizational operations automation.
"""

__version__ = "0.1.0"

from .core.chief_agent import ChiefAgent
from .core.slave_agent import SlaveAgent
from .protocols.a2a_protocol import A2AProtocol
from .protocols.mcp_protocol import MCPProtocol
from .interfaces.employee_interface import EmployeeInterface
from .interfaces.customer_interface import CustomerInterface

__all__ = [
    "ChiefAgent",
    "SlaveAgent",
    "A2AProtocol",
    "MCPProtocol",
    "EmployeeInterface",
    "CustomerInterface",
]
