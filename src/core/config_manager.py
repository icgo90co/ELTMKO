"""
Configuration Manager Module
Handles loading and validation of configuration files
"""
import os
import yaml
import logging
from typing import Dict, Any, List
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration from YAML and environment variables"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize configuration manager
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = config_path
        self.config = {}
        load_dotenv()
        self._load_config()
        
    def _load_config(self):
        """Load configuration from YAML file and substitute environment variables"""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            with open(config_file, 'r') as f:
                raw_config = yaml.safe_load(f)
            
            # Substitute environment variables
            self.config = self._substitute_env_vars(raw_config)
            logger.info(f"Configuration loaded from {self.config_path}")
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    def _substitute_env_vars(self, obj: Any) -> Any:
        """
        Recursively substitute ${VAR} patterns with environment variables
        
        Args:
            obj: Configuration object (dict, list, or primitive)
            
        Returns:
            Object with substituted values
        """
        if isinstance(obj, dict):
            return {k: self._substitute_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._substitute_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            # Replace ${VAR} with environment variable value
            if obj.startswith("${") and obj.endswith("}"):
                var_name = obj[2:-1]
                return os.getenv(var_name, obj)
            return obj
        else:
            return obj
    
    def get_destinations(self) -> List[Dict[str, Any]]:
        """Get all configured destinations"""
        return self.config.get('destinations', [])
    
    def get_destination(self, name: str) -> Dict[str, Any]:
        """
        Get specific destination configuration by name
        
        Args:
            name: Destination name
            
        Returns:
            Destination configuration dict
        """
        destinations = self.get_destinations()
        for dest in destinations:
            if dest.get('name') == name:
                return dest
        raise ValueError(f"Destination '{name}' not found in configuration")
    
    def get_sources(self) -> List[Dict[str, Any]]:
        """Get all configured sources"""
        return self.config.get('sources', [])
    
    def get_source(self, name: str) -> Dict[str, Any]:
        """
        Get specific source configuration by name
        
        Args:
            name: Source name
            
        Returns:
            Source configuration dict
        """
        sources = self.get_sources()
        for source in sources:
            if source.get('name') == name:
                return source
        raise ValueError(f"Source '{name}' not found in configuration")
    
    def get_enabled_sources(self) -> List[Dict[str, Any]]:
        """Get only enabled sources"""
        return [s for s in self.get_sources() if s.get('enabled', False)]
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self.config.get('logging', {})
    
    def reload(self):
        """Reload configuration from file"""
        self._load_config()
        logger.info("Configuration reloaded")
