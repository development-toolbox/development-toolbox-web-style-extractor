"""
Hybrid format metadata manager
Combines format_configs.py fallbacks with plugin-specific metadata
"""

from typing import Dict, Any, Optional, List
from format_configs import get_format_config, FORMAT_CONFIGS


class FormatManager:
    """Manages format metadata with hybrid approach"""
    
    def __init__(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self._cache = {}
    
    def get_available_formats(self) -> List[str]:
        """Get all available output formats from discovered generator plugins"""
        generators = self.plugin_manager.get_generators()
        return [gen.output_format for gen in generators]
    
    def get_format_metadata(self, format_name: str) -> Dict[str, Any]:
        """
        Get metadata for a format with hybrid fallback:
        1. Try plugin metadata first
        2. Fall back to format_configs.py
        3. Return minimal defaults if neither exists
        """
        if format_name in self._cache:
            return self._cache[format_name]
        
        # Try to find generator plugin
        generators = self.plugin_manager.get_generators()
        plugin = None
        for gen in generators:
            if gen.output_format == format_name:
                plugin = gen
                break
        
        # Get base config from format_configs.py
        base_config = get_format_config(format_name)
        
        # Override with plugin metadata if available
        metadata = base_config.copy()
        
        if plugin:
            # Plugin metadata overrides format_configs.py
            if plugin.description:
                metadata['description'] = plugin.description
            if plugin.emoji:
                metadata['emoji'] = plugin.emoji
            if plugin.short_description:
                metadata['short_description'] = plugin.short_description
            if plugin.full_description:
                metadata['full_description'] = plugin.full_description
            if plugin.file_extension:
                metadata['file_extension'] = plugin.file_extension
            if plugin.capabilities:
                metadata['capabilities'] = plugin.capabilities
            if plugin.use_cases:
                metadata['use_cases'] = plugin.use_cases
                
        # Cache result
        self._cache[format_name] = metadata
        return metadata
    
    def get_default_format(self) -> str:
        """Get default format - prefer MediaWiki if available, otherwise first available"""
        available = self.get_available_formats()
        
        if not available:
            raise RuntimeError("No generator plugins available")
            
        # Prefer MediaWiki as default
        if 'mediawiki' in available:
            return 'mediawiki'
            
        # Otherwise return first available
        return available[0]
    
    def get_format_choices_for_cli(self) -> List[str]:
        """Get format choices for CLI argument parser"""
        return self.get_available_formats()
    
    def get_format_descriptions_for_help(self) -> str:
        """Generate format descriptions for CLI help text"""
        available = self.get_available_formats()
        lines = []
        
        for fmt in available:
            metadata = self.get_format_metadata(fmt)
            emoji = metadata.get('emoji', '')
            short_desc = metadata.get('short_description', 'No description')
            lines.append(f"  {fmt:<12} {emoji} {short_desc}")
        
        return "\n".join(lines)
    
    def is_format_available(self, format_name: str) -> bool:
        """Check if format is available via plugins"""
        return format_name in self.get_available_formats()