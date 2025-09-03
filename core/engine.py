"""
Minimal extraction engine - orchestrates plugins but does no extraction itself
"""
import requests
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import selenium.common.exceptions
from typing import Dict, Any, Optional, List
from .plugin_manager import PluginManager
from .format_manager import FormatManager


class WebStyleExtractorEngine:
    """Core extraction engine that orchestrates plugin execution"""
    
    def __init__(self):
        self.plugin_manager = PluginManager()
        self.format_manager = FormatManager(self.plugin_manager)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract(self, url: str, enabled_extractors: Optional[List[str]] = None, enabled_generators: Optional[List[str]] = None, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Main extraction method using plugin system"""
        
        # Setup web driver and soup
        driver = self._setup_webdriver()
        soup = self._get_soup(url)
        
        if not soup:
            logging.error(f"Failed to fetch page content from {url}")
            return {}
        
        try:
            # Run extraction plugins
            extraction_results = {}
            extractors = enabled_extractors or self.plugin_manager.get_available_extractors()
            
            for extractor_name in extractors:
                extractor = self.plugin_manager.get_extractor(extractor_name)
                if extractor:
                    logging.info(f"Running extractor: {extractor_name}")
                    try:
                        extraction_results[extractor_name] = extractor.extract(soup, driver, url)
                    except Exception as e:
                        logging.error(f"Error in {extractor_name}: {e}")
                        extraction_results[extractor_name] = {}
            
            # Run generator plugins
            generation_results = {}
            generators = enabled_generators or self.plugin_manager.get_available_generators()
            
            # Package data for generators - include full results structure
            generator_data = {
                'url': url,
                'extraction': extraction_results,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            for generator_name in generators:
                generator = self.plugin_manager.get_generator(generator_name)
                if generator:
                    logging.info(f"Running generator: {generator_name}")
                    try:
                        generation_results[generator_name] = generator.generate(generator_data, output_path)
                    except Exception as e:
                        logging.error(f"Error in {generator_name}: {e}")
                        generation_results[generator_name] = {}
            
            return {
                'url': url,
                'extraction': extraction_results,
                'generation': generation_results,
                'metadata': {
                    'extractors_used': list(extraction_results.keys()),
                    'generators_used': list(generation_results.keys())
                }
            }
            
        finally:
            if driver:
                driver.quit()
    
    def _setup_webdriver(self) -> Optional[webdriver.Chrome]:
        """Setup Chrome WebDriver for dynamic extraction"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--log-level=3')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
            
        except selenium.common.exceptions.WebDriverException as e:
            logging.warning(f"WebDriver setup failed: {e}. Falling back to static extraction only.")
            return None
    
    def _get_soup(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse HTML content"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logging.error(f"Failed to fetch {url}: {e}")
            return None
    
    def list_available_plugins(self) -> Dict[str, List[str]]:
        """List all available plugins"""
        return self.plugin_manager.list_plugins()
        
    def get_available_formats(self) -> List[str]:
        """Get available output formats"""
        return self.format_manager.get_available_formats()
        
    def get_default_format(self) -> str:
        """Get default output format"""
        return self.format_manager.get_default_format()
        
    def get_format_metadata(self, format_name: str) -> Dict[str, Any]:
        """Get metadata for a specific format"""
        return self.format_manager.get_format_metadata(format_name)
        
    def get_format_choices_for_cli(self) -> List[str]:
        """Get format choices for CLI"""
        return self.format_manager.get_format_choices_for_cli()
        
    def get_format_descriptions_for_help(self) -> str:
        """Get format descriptions for CLI help"""
        return self.format_manager.get_format_descriptions_for_help()