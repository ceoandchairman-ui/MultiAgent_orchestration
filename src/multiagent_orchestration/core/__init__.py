"""Core module for agent definitions and orchestration logic."""

from .chief_agent import ChiefAgent
from .slave_agent import SlaveAgent
from .agent_registry import AgentRegistry

__all__ = ["ChiefAgent", "SlaveAgent", "AgentRegistry"]
