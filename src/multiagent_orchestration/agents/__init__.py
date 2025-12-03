"""Pre-configured agent implementations for different departments."""

from .hr_agent import HRAgent
from .finance_agent import FinanceAgent
from .support_agent import SupportAgent
from .operations_agent import OperationsAgent

__all__ = ["HRAgent", "FinanceAgent", "SupportAgent", "OperationsAgent"]
