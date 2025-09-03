"""
Core module for Web Style Extractor plugin system
"""
from .engine import WebStyleExtractorEngine
from .plugin_manager import PluginManager

__all__ = ['WebStyleExtractorEngine', 'PluginManager']