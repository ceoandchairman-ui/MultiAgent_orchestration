"""Configuration management for the orchestration system."""

import os
import yaml
from typing import Any, Dict, Optional
from pathlib import Path


class Config:
    """
    Configuration manager for the orchestration system.
    
    Loads configuration from files and environment variables.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.config: Dict[str, Any] = self._load_default_config()
        
        if config_file:
            self._load_from_file(config_file)
        
        self._load_from_env()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            "system": {
                "name": "MultiAgent Orchestration System",
                "version": "0.1.0",
                "environment": "development"
            },
            "agents": {
                "chief": {
                    "enabled": True,
                    "max_concurrent_tasks": 100
                },
                "slave": {
                    "enabled": True,
                    "auto_register": True
                }
            },
            "protocols": {
                "a2a": {
                    "queue_size": 1000,
                    "timeout": 30
                },
                "mcp": {
                    "context_size": 10000,
                    "history_size": 100
                }
            },
            "interfaces": {
                "employee": {
                    "enabled": True,
                    "session_timeout": 3600
                },
                "customer": {
                    "enabled": True,
                    "guest_access": True,
                    "session_timeout": 1800
                }
            },
            "logging": {
                "level": "INFO",
                "json_format": True,
                "file": None
            }
        }
    
    def _load_from_file(self, config_file: str) -> None:
        """
        Load configuration from a YAML file.
        
        Args:
            config_file: Path to configuration file
        """
        config_path = Path(config_file)
        
        if not config_path.exists():
            print(f"Config file not found: {config_file}")
            return
        
        try:
            with open(config_path, 'r') as f:
                file_config = yaml.safe_load(f)
                self._merge_config(file_config)
        except Exception as e:
            print(f"Error loading config file: {e}")
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # System - Check if environment variable exists and use it if it does
        if env_val := os.getenv("ORCHESTRATION_ENV"):
            self.config["system"]["environment"] = env_val
        
        # Logging - Check if log level is set in environment
        if env_val := os.getenv("LOG_LEVEL"):
            self.config["logging"]["level"] = env_val
        
        # Check if JSON format preference is set in environment
        if env_val := os.getenv("LOG_JSON"):
            self.config["logging"]["json_format"] = env_val.lower() == "true"
    
    def _merge_config(self, new_config: Dict[str, Any]) -> None:
        """
        Merge new configuration with existing.
        
        Args:
            new_config: New configuration to merge
        """
        def merge_dict(base: Dict, updates: Dict) -> Dict:
            for key, value in updates.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
            return base
        
        merge_dict(self.config, new_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'system.version')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get all configuration as a dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self.config.copy()
