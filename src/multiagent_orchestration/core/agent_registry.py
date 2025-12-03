"""
Agent Registry

Central registry for managing all agents in the system.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class AgentRegistry:
    """
    Centralized registry for tracking all agents in the orchestration system.
    
    Provides discovery, lookup, and management capabilities.
    """
    
    def __init__(self):
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.chief_agents: List[str] = []
        self.slave_agents: Dict[str, List[str]] = {}  # Organized by department
        
    def register_agent(
        self,
        agent_id: str,
        agent_type: str,
        capabilities: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Register an agent in the registry.
        
        Args:
            agent_id: Unique agent identifier
            agent_type: Type of agent
            capabilities: Agent capabilities
            metadata: Additional metadata
            
        Returns:
            Registration result
        """
        agent_info = {
            "agent_id": agent_id,
            "agent_type": agent_type,
            "capabilities": capabilities,
            "metadata": metadata or {},
            "registered_at": datetime.utcnow().isoformat(),
            "status": "active"
        }
        
        self.agents[agent_id] = agent_info
        
        # Track by type
        if agent_type == "chief":
            self.chief_agents.append(agent_id)
        else:
            department = metadata.get("department", "general") if metadata else "general"
            if department not in self.slave_agents:
                self.slave_agents[department] = []
            self.slave_agents[department].append(agent_id)
        
        return {
            "status": "success",
            "agent_id": agent_id,
            "registered_at": agent_info["registered_at"]
        }
    
    def unregister_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Unregister an agent from the registry.
        
        Args:
            agent_id: Agent to unregister
            
        Returns:
            Result of unregistration
        """
        if agent_id not in self.agents:
            return {"status": "error", "message": "Agent not found"}
        
        agent_info = self.agents[agent_id]
        
        # Remove from tracking lists
        if agent_info["agent_type"] == "chief":
            self.chief_agents.remove(agent_id)
        else:
            department = agent_info["metadata"].get("department", "general")
            if department in self.slave_agents:
                self.slave_agents[department].remove(agent_id)
        
        del self.agents[agent_id]
        
        return {
            "status": "success",
            "agent_id": agent_id,
            "unregistered_at": datetime.utcnow().isoformat()
        }
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Agent information or None
        """
        return self.agents.get(agent_id)
    
    def get_agents_by_type(self, agent_type: str) -> List[Dict[str, Any]]:
        """
        Get all agents of a specific type.
        
        Args:
            agent_type: Type of agents to retrieve
            
        Returns:
            List of agent information
        """
        return [
            agent for agent in self.agents.values()
            if agent["agent_type"] == agent_type
        ]
    
    def get_agents_by_department(self, department: str) -> List[Dict[str, Any]]:
        """
        Get all agents in a specific department.
        
        Args:
            department: Department name
            
        Returns:
            List of agent information
        """
        agent_ids = self.slave_agents.get(department, [])
        return [self.agents[agent_id] for agent_id in agent_ids if agent_id in self.agents]
    
    def get_agents_by_capability(self, capability: str) -> List[Dict[str, Any]]:
        """
        Find agents with a specific capability.
        
        Args:
            capability: Required capability
            
        Returns:
            List of agents with the capability
        """
        return [
            agent for agent in self.agents.values()
            if capability in agent["capabilities"]
        ]
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """
        Get all registered agents.
        
        Returns:
            List of all agent information
        """
        return list(self.agents.values())
    
    def get_chief_agents(self) -> List[Dict[str, Any]]:
        """
        Get all chief agents.
        
        Returns:
            List of chief agent information
        """
        return [self.agents[agent_id] for agent_id in self.chief_agents]
    
    def get_departments(self) -> List[str]:
        """
        Get list of all departments.
        
        Returns:
            List of department names
        """
        return list(self.slave_agents.keys())
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the registry.
        
        Returns:
            Registry statistics
        """
        return {
            "total_agents": len(self.agents),
            "chief_agents": len(self.chief_agents),
            "departments": len(self.slave_agents),
            "department_breakdown": {
                dept: len(agents) for dept, agents in self.slave_agents.items()
            },
            "timestamp": datetime.utcnow().isoformat()
        }
