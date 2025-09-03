"""
Abstract base classes that all plugins must implement
"""
import shutil
from datetime import datetime
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseExtractor(ABC):
    """Base class for all extractor plugins"""
    
    @abstractmethod
    def extract(self, soup, driver, url: str) -> Dict[str, Any]:
        """
        Extract data from webpage
        
        Args:
            soup: BeautifulSoup parsed HTML
            driver: Selenium WebDriver (may be None if WebDriver setup failed)
            url: URL being processed
            
        Returns:
            Dictionary containing extracted data
        """
        pass
    
    @property
    @abstractmethod 
    def name(self) -> str:
        """Plugin name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description"""
        pass


class BaseGenerator(ABC):
    """Base class for all generator plugins"""
    
    @abstractmethod
    def generate(self, extraction_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
        """
        Generate output from extraction data
        
        Args:
            extraction_data: Combined data from all extractors
            output_path: Optional output directory path
            
        Returns:
            Dictionary containing generation results
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name"""
        pass
    
    @property
    @abstractmethod
    def output_format(self) -> str:
        """Output format/extension"""
        pass
    
    @property
    def description(self) -> str:
        """Plugin description - optional, fallback to format_configs.py"""
        return None
    
    @property 
    def emoji(self) -> str:
        """Format emoji - optional, fallback to format_configs.py"""
        return None
        
    @property
    def short_description(self) -> str:
        """Short description - optional, fallback to format_configs.py"""
        return None
        
    @property
    def full_description(self) -> str:
        """Full description - optional, fallback to format_configs.py"""
        return None
        
    @property
    def file_extension(self) -> str:
        """File extension - optional, fallback to format_configs.py"""
        return self.output_format
        
    @property
    def capabilities(self) -> list:
        """List of capabilities - optional, fallback to format_configs.py"""
        return None
        
    @property
    def use_cases(self) -> list:
        """List of use cases - optional, fallback to format_configs.py"""
        return None
    
    def archive_existing_file(self, file_path: Path, format_dir: Path):
        """Archive existing file with timestamp - shared utility method"""
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        archive_dir = format_dir / 'archive' / timestamp
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        archive_path = archive_dir / file_path.name
        shutil.move(str(file_path), str(archive_path))
        print(f"📦 Archived {file_path.name} to archive/{timestamp}/")