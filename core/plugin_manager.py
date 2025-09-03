"""
Plugin discovery, loading, and registry management
"""
import importlib
import os
import yaml
import logging
from typing import Dict, List, Optional


class PluginManager:
    """Manages plugin discovery, loading, and registry"""
    
    def __init__(self):
        self.extractors = {}
        self.generators = {}
        self.loaded_plugins = set()
        self._load_plugin_config()
        self.discover_plugins()
    
    def _load_plugin_config(self):
        """Load plugin configuration from plugins.yaml"""
        config_path = 'config/plugins.yaml'
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {
                'enabled_extractors': ['html_extractor', 'color_extractor', 'font_extractor', 'css_extractor'],
                'enabled_generators': ['json_generator', 'css_generator']
            }
    
    def discover_plugins(self):
        """Auto-discover all available plugins"""
        # Discover extractor plugins
        extractor_path = 'plugins/extractors'
        if os.path.exists(extractor_path):
            for item in os.listdir(extractor_path):
                if os.path.isdir(os.path.join(extractor_path, item)) and not item.startswith('__'):
                    self._register_extractor(item)
        
        # Discover generator plugins
        generator_path = 'plugins/generators'
        if os.path.exists(generator_path):
            for item in os.listdir(generator_path):
                if os.path.isdir(os.path.join(generator_path, item)) and not item.startswith('__'):
                    self._register_generator(item)
    
    def _register_extractor(self, plugin_name: str):
        """Register an extractor plugin"""
        try:
            module = importlib.import_module(f'plugins.extractors.{plugin_name}.plugin')
            if hasattr(module, 'get_extractor'):
                extractor = module.get_extractor()
                self.extractors[plugin_name] = extractor
                self.loaded_plugins.add(plugin_name)
                logging.debug(f"Loaded extractor plugin: {plugin_name}")
        except ImportError as e:
            logging.warning(f"Failed to load extractor plugin {plugin_name}: {e}")
        except Exception as e:
            logging.error(f"Error loading extractor plugin {plugin_name}: {e}")
    
    def _register_generator(self, plugin_name: str):
        """Register a generator plugin"""
        try:
            module = importlib.import_module(f'plugins.generators.{plugin_name}.plugin')
            if hasattr(module, 'get_generator'):
                generator = module.get_generator()
                self.generators[plugin_name] = generator
                self.loaded_plugins.add(plugin_name)
                logging.debug(f"Loaded generator plugin: {plugin_name}")
        except ImportError as e:
            logging.warning(f"Failed to load generator plugin {plugin_name}: {e}")
        except Exception as e:
            logging.error(f"Error loading generator plugin {plugin_name}: {e}")
    
    def get_extractor(self, name: str):
        """Get an extractor plugin by name"""
        return self.extractors.get(name)
    
    def get_generator(self, name: str):
        """Get a generator plugin by name"""
        return self.generators.get(name)
    
    def get_available_extractors(self) -> List[str]:
        """Get list of available extractor plugin names"""
        enabled = self.config.get('enabled_extractors', [])
        if enabled:
            return [name for name in enabled if name in self.extractors]
        return list(self.extractors.keys())
    
    def get_available_generators(self) -> List[str]:
        """Get list of available generator plugin names"""
        # For a pluggable system, all loaded generators should be available
        return list(self.generators.keys())
    
    def get_generators(self) -> List:
        """Get list of generator plugin instances"""
        return list(self.generators.values())
    
    def list_plugins(self) -> Dict[str, List[str]]:
        """List all available plugins"""
        return {
            'extractors': list(self.extractors.keys()),
            'generators': list(self.generators.keys()),
            'loaded': list(self.loaded_plugins)
        }
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, str]]:
        """Get information about a specific plugin"""
        if plugin_name in self.extractors:
            plugin = self.extractors[plugin_name]
            return {
                'name': plugin.name,
                'type': 'extractor',
                'description': plugin.description
            }
        elif plugin_name in self.generators:
            plugin = self.generators[plugin_name]
            return {
                'name': plugin.name,
                'type': 'generator',
                'output_format': plugin.output_format
            }
        return None