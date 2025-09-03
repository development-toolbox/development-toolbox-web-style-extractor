# Komplett Instruktioner för Claude Code Agent: Web Style Extractor Plugin Refaktorering

## 🎯 Mål: Refaktorera till komplett plugin-arkitektur + lägg till BookStack + GitHub Pages

**Total tid: 1-2 timmar**
- Refaktorera ALL funktionalitet till plugins
- Lägg till BookStack generator plugin  
- Lägg till GitHub Pages generator för projekt-website
- Generera riktiga exempel genom att köra verktyget

---

## 📁 Komplett Ny Struktur

```
web_style_extractor/
├── core/
│   ├── __init__.py
│   ├── engine.py              # Minimal extraction engine (~200 rader)
│   └── plugin_manager.py      # Plugin discovery/loading (~150 rader)
├── plugins/
│   ├── __init__.py
│   ├── base_plugin.py         # Abstract base classes för plugins
│   │
│   ├── extractors/            # ALLA extraction funktioner som plugins
│   │   ├── __init__.py
│   │   ├── html_extractor/
│   │   │   ├── __init__.py
│   │   │   ├── plugin.py      # HTML parsing + DOM analysis
│   │   │   ├── README.md      # HTML extraction dokumentation
│   │   │   ├── config.yaml    # Plugin konfiguration
│   │   │   └── tests/         # Plugin-specifika tester
│   │   ├── color_extractor/
│   │   │   ├── plugin.py      # Färg extraction från CSS/computed styles
│   │   │   ├── README.md      # Färg-algoritmer dokumentation
│   │   │   ├── config.yaml
│   │   │   └── tests/
│   │   ├── font_extractor/
│   │   │   ├── plugin.py      # Font detection från CSS
│   │   │   ├── README.md      # Typography extraction guide
│   │   │   ├── config.yaml
│   │   │   └── tests/
│   │   ├── css_extractor/
│   │   │   ├── plugin.py      # CSS rules parsing
│   │   │   ├── README.md      # CSS analysis dokumentation
│   │   │   ├── config.yaml
│   │   │   └── tests/
│   │   └── branding_extractor/
│   │       ├── plugin.py      # Logo, favicon, brand elements
│   │       ├── README.md      # Branding detection guide
│   │       ├── config.yaml
│   │       └── tests/
│   │
│   └── generators/            # ALLA output format som plugins
│       ├── __init__.py
│       ├── json_generator/
│       │   ├── plugin.py      # JSON output generation
│       │   ├── README.md      # JSON schema dokumentation
│       │   ├── config.yaml
│       │   ├── templates/
│       │   │   └── output.jinja2
│       │   └── tests/
│       ├── css_generator/
│       │   ├── plugin.py      # CSS variables generation
│       │   ├── README.md      # CSS output format guide
│       │   ├── config.yaml
│       │   ├── templates/
│       │   │   └── styles.jinja2
│       │   └── tests/
│       ├── mediawiki_generator/
│       │   ├── plugin.py      # MediaWiki template generation
│       │   ├── README.md      # MediaWiki usage guide
│       │   ├── config.yaml
│       │   ├── templates/
│       │   │   ├── wiki_page.jinja2
│       │   │   └── color_table.jinja2
│       │   └── tests/
│       ├── tailwind_generator/
│       │   ├── plugin.py      # Tailwind config generation
│       │   ├── README.md      # Tailwind integration guide
│       │   ├── config.yaml
│       │   ├── templates/
│       │   │   └── tailwind.config.jinja2
│       │   └── tests/
│       ├── bookstack_generator/
│       │   ├── plugin.py      # BookStack CSS theme + assets
│       │   ├── README.md      # BookStack installation guide
│       │   ├── config.yaml
│       │   ├── templates/
│       │   │   ├── bookstack.css.jinja2
│       │   │   └── installation.md.jinja2
│       │   ├── assets/
│       │   │   └── default-logo.png
│       │   └── tests/
│       └── github_pages_generator/
│           ├── plugin.py      # GitHub Pages för DETTA projekt
│           ├── README.md      # GitHub Pages setup guide
│           ├── config.yaml
│           ├── templates/
│           │   ├── index.html.jinja2     # Project landing page
│           │   ├── demo.html.jinja2      # Live demo showcase
│           │   ├── docs.html.jinja2      # Documentation site
│           │   └── examples.html.jinja2  # Examples showcase
│           ├── assets/
│           │   ├── styles.css
│           │   └── app.js
│           └── tests/
├── projects/                  # RIKTIGA exempel genererade av verktyget
│   ├── README.md             # "Dessa exempel genereras genom att köra verktyget"
│   ├── google.com/           # python style_extractor.py https://google.com --all-formats
│   │   ├── metadata.txt      # Automatiskt genererat
│   │   ├── styles.json       # Automatiskt genererat
│   │   ├── styles.css        # Automatiskt genererat
│   │   ├── styles.mediawiki  # Automatiskt genererat
│   │   ├── tailwind.config.js # Automatiskt genererat
│   │   ├── bookstack_template/
│   │   │   ├── custom.css
│   │   │   ├── assets/
│   │   │   └── README.md
│   │   └── github_pages/
│   │       ├── index.html
│   │       └── assets/
│   ├── github.com/           # python style_extractor.py https://github.com --all-formats
│   ├── stripe.com/           # python style_extractor.py https://stripe.com --all-formats
│   ├── airbnb.com/           # python style_extractor.py https://airbnb.com --all-formats
│   └── shopify.com/          # python style_extractor.py https://shopify.com --all-formats
├── docs/
│   ├── README.md              # Huvuddokumentation
│   ├── installation.md       # Installation guide
│   ├── user-guide.md          # Användarguide
│   ├── plugin-development.md  # Hur man utvecklar plugins
│   ├── api-reference.md       # API dokumentation
│   ├── examples/
│   │   ├── basic-usage.md
│   │   ├── bookstack-setup.md
│   │   ├── github-pages-setup.md
│   │   └── custom-plugins.md
│   ├── output-formats/
│   │   ├── json-format.md
│   │   ├── css-format.md
│   │   ├── mediawiki-format.md
│   │   ├── tailwind-format.md
│   │   ├── bookstack-format.md
│   │   └── github-pages-format.md
│   └── troubleshooting.md
├── templates/                 # Global fallback templates
│   ├── base.jinja2
│   └── common/
│       ├── colors.jinja2
│       └── fonts.jinja2
├── config/
│   ├── plugins.yaml           # Vilka plugins ska laddas
│   └── settings.yaml          # Global settings
├── tests/
│   ├── test_core.py
│   ├── test_plugin_manager.py
│   └── plugins/               # Plugin-specifika tester kopieras hit
├── requirements.txt           # Lägg till: Pillow, Jinja2, PyYAML
├── setup.py                  # Package setup
└── style_extractor.py         # Refaktorerad CLI som använder plugin system
```

---

## 🔧 Implementation Steps

### 1. Skapa Plugin System Foundation (30 min)

**A. Core Engine** (`core/engine.py`):
```python
"""
Minimal extraction engine - orkestrera plugins men gör ingen extraction själv
"""
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from core.plugin_manager import PluginManager

class WebStyleExtractorEngine:
    def __init__(self):
        self.plugin_manager = PluginManager()
    
    def extract(self, url, enabled_extractors=None, enabled_generators=None):
        """Main extraction method using plugin system"""
        
        # Setup web driver and soup (FLYTTA FRÅN BEFINTLIG KOD)
        driver = self._setup_webdriver()  
        soup = self._get_soup(url)
        
        try:
            # Run extraction plugins
            extraction_results = {}
            extractors = enabled_extractors or self.plugin_manager.get_available_extractors()
            
            for extractor_name in extractors:
                extractor = self.plugin_manager.get_extractor(extractor_name)
                if extractor:
                    extraction_results[extractor_name] = extractor.extract(soup, driver, url)
            
            # Run generator plugins
            generation_results = {}
            generators = enabled_generators or self.plugin_manager.get_available_generators()
            
            for generator_name in generators:
                generator = self.plugin_manager.get_generator(generator_name)
                if generator:
                    generation_results[generator_name] = generator.generate(extraction_results)
            
            return {
                'extraction': extraction_results,
                'generation': generation_results
            }
            
        finally:
            driver.quit()
    
    def _setup_webdriver(self):
        # FLYTTA BEFINTLIG WEBDRIVER SETUP HIT
        pass
    
    def _get_soup(self, url):
        # FLYTTA BEFINTLIG BEAUTIFULSOUP SETUP HIT  
        pass
```

**B. Plugin Manager** (`core/plugin_manager.py`):
```python
"""
Plugin discovery, loading, and registry management
"""
import importlib
import os
import yaml
from typing import Dict, List

class PluginManager:
    def __init__(self):
        self.extractors = {}
        self.generators = {}
        self.loaded_plugins = set()
        self._load_plugin_config()
    
    def _load_plugin_config(self):
        """Load plugin configuration from plugins.yaml"""
        config_path = 'config/plugins.yaml'
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {'enabled_extractors': [], 'enabled_generators': []}
    
    def discover_plugins(self):
        """Auto-discover all available plugins"""
        # Discover extractor plugins
        extractor_path = 'plugins/extractors'
        for item in os.listdir(extractor_path):
            if os.path.isdir(os.path.join(extractor_path, item)) and not item.startswith('__'):
                self._register_extractor(item)
        
        # Discover generator plugins
        generator_path = 'plugins/generators'  
        for item in os.listdir(generator_path):
            if os.path.isdir(os.path.join(generator_path, item)) and not item.startswith('__'):
                self._register_generator(item)
    
    def _register_extractor(self, plugin_name):
        """Register an extractor plugin"""
        try:
            module = importlib.import_module(f'plugins.extractors.{plugin_name}.plugin')
            if hasattr(module, 'get_extractor'):
                self.extractors[plugin_name] = module.get_extractor()
                self.loaded_plugins.add(plugin_name)
        except ImportError as e:
            print(f"Failed to load extractor plugin {plugin_name}: {e}")
    
    def _register_generator(self, plugin_name):
        """Register a generator plugin"""
        try:
            module = importlib.import_module(f'plugins.generators.{plugin_name}.plugin')
            if hasattr(module, 'get_generator'):
                self.generators[plugin_name] = module.get_generator()
                self.loaded_plugins.add(plugin_name)
        except ImportError as e:
            print(f"Failed to load generator plugin {plugin_name}: {e}")
    
    def get_extractor(self, name):
        return self.extractors.get(name)
    
    def get_generator(self, name):
        return self.generators.get(name)
    
    def get_available_extractors(self):
        return list(self.extractors.keys())
    
    def get_available_generators(self):
        return list(self.generators.keys())
    
    def list_plugins(self):
        """List all available plugins"""
        return {
            'extractors': self.get_available_extractors(),
            'generators': self.get_available_generators()
        }
```

**C. Base Plugin Classes** (`plugins/base_plugin.py`):
```python
"""
Abstract base classes som alla plugins måste implementera
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseExtractor(ABC):
    """Base class för alla extractor plugins"""
    
    @abstractmethod
    def extract(self, soup, driver, url) -> Dict[str, Any]:
        """Extract data from webpage"""
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
    """Base class för alla generator plugins"""
    
    @abstractmethod
    def generate(self, extraction_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
        """Generate output from extraction data"""
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
```

### 2. Flytta Befintlig Funktionalitet till Plugins (45 min)

**A. Color Extractor Plugin** (`plugins/extractors/color_extractor/plugin.py`):
```python
"""
Color extraction plugin - FLYTTA ALL FÄRG-LOGIK FRÅN BEFINTLIG WEBSTYLEEXTRACTOR
"""
from plugins.base_plugin import BaseExtractor

class ColorExtractor(BaseExtractor):
    @property
    def name(self):
        return "color_extractor"
    
    @property
    def description(self):
        return "Extracts colors from CSS and computed styles"
    
    def extract(self, soup, driver, url):
        """
        FLYTTA ALL BEFINTLIG FÄRG-EXTRACTION LOGIK HIT:
        - CSS color parsing
        - Computed style analysis  
        - Color deduplication
        - Color sorting/prioritering
        """
        colors = []
        
        # TODO: FLYTTA BEFINTLIG FÄRG-EXTRACTION LOGIK FRÅN WebStyleExtractor
        # - driver.execute_script för computed styles
        # - CSS parsing för färg-värden
        # - Färg-konvertering och deduplicering
        
        return {
            'colors': colors,
            'primary_color': colors[0] if colors else None,
            'color_palette': self._generate_palette(colors)
        }
    
    def _generate_palette(self, colors):
        # FLYTTA BEFINTLIG FÄRG-PALETTE LOGIK
        pass

def get_extractor():
    return ColorExtractor()
```

**B. Font Extractor Plugin** (`plugins/extractors/font_extractor/plugin.py`):
```python
"""
Font extraction plugin - FLYTTA ALL FONT-LOGIK FRÅN BEFINTLIG KOD
"""
from plugins.base_plugin import BaseExtractor

class FontExtractor(BaseExtractor):
    @property
    def name(self):
        return "font_extractor"
    
    @property
    def description(self):
        return "Extracts typography and font information"
    
    def extract(self, soup, driver, url):
        """
        FLYTTA ALL BEFINTLIG FONT-EXTRACTION LOGIK HIT:
        - CSS font parsing
        - Computed font styles
        - Font family detection
        - Typography hierarchy
        """
        fonts = []
        
        # TODO: FLYTTA BEFINTLIG FONT-EXTRACTION FRÅN WebStyleExtractor
        # - Font family detection
        # - Font size analysis
        # - Typography hierarchy
        
        return {
            'fonts': fonts,
            'primary_font': fonts[0] if fonts else None,
            'typography_scale': self._analyze_typography_scale(fonts)
        }
    
    def _analyze_typography_scale(self, fonts):
        # FLYTTA BEFINTLIG TYPOGRAPHY ANALYSIS
        pass

def get_extractor():
    return FontExtractor()
```

**C. CSS Extractor Plugin** (`plugins/extractors/css_extractor/plugin.py`):
```python
"""
CSS parsing and analysis plugin
"""
from plugins.base_plugin import BaseExtractor

class CSSExtractor(BaseExtractor):
    @property
    def name(self):
        return "css_extractor"
    
    @property
    def description(self):
        return "Extracts and analyzes CSS rules and properties"
    
    def extract(self, soup, driver, url):
        """Extract CSS rules, selectors, and properties"""
        
        # TODO: FLYTTA CSS PARSING LOGIK FRÅN BEFINTLIG KOD
        # - CSS rule extraction
        # - Selector analysis
        # - Property parsing
        
        return {
            'css_rules': [],
            'selectors': [],
            'properties': {},
            'media_queries': []
        }

def get_extractor():
    return CSSExtractor()
```

**D. HTML Extractor Plugin** (`plugins/extractors/html_extractor/plugin.py`):
```python
"""
HTML structure and DOM analysis plugin
"""
from plugins.base_plugin import BaseExtractor

class HTMLExtractor(BaseExtractor):
    @property
    def name(self):
        return "html_extractor"
    
    @property
    def description(self):
        return "Extracts HTML structure and DOM information"
    
    def extract(self, soup, driver, url):
        """Extract HTML structure and metadata"""
        
        return {
            'title': soup.title.string if soup.title else None,
            'meta_description': self._get_meta_description(soup),
            'headings': self._extract_headings(soup),
            'dom_structure': self._analyze_dom_structure(soup)
        }
    
    def _get_meta_description(self, soup):
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta.get('content') if meta else None
    
    def _extract_headings(self, soup):
        headings = {}
        for level in range(1, 7):
            headings[f'h{level}'] = [h.get_text().strip() for h in soup.find_all(f'h{level}')]
        return headings
    
    def _analyze_dom_structure(self, soup):
        # Basic DOM analysis
        return {
            'total_elements': len(soup.find_all()),
            'classes': list(set([cls for el in soup.find_all() for cls in el.get('class', [])])),
            'ids': list(set([el.get('id') for el in soup.find_all() if el.get('id')]))
        }

def get_extractor():
    return HTMLExtractor()
```

### 3. Skapa Generator Plugins (45 min)

**A. JSON Generator** (`plugins/generators/json_generator/plugin.py`):
```python
"""
JSON output generator - FLYTTA FRÅN BEFINTLIG KOD
"""
from plugins.base_plugin import BaseGenerator
import json
import os

class JSONGenerator(BaseGenerator):
    @property
    def name(self):
        return "json_generator"
    
    @property
    def output_format(self):
        return "json"
    
    def generate(self, extraction_data, output_path=None):
        """Generate JSON output from extraction data"""
        
        # TODO: FLYTTA BEFINTLIG JSON GENERATION LOGIK
        
        output = {
            'metadata': {
                'generated_by': 'Web Style Extractor',
                'timestamp': self._get_timestamp()
            },
            'data': extraction_data
        }
        
        if output_path:
            json_path = os.path.join(output_path, 'styles.json')
            with open(json_path, 'w') as f:
                json.dump(output, f, indent=2)
            return {'file': json_path}
        
        return output
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

def get_generator():
    return JSONGenerator()
```

**B. CSS Generator** (`plugins/generators/css_generator/plugin.py`):
```python
"""
CSS variables generator - FLYTTA FRÅN BEFINTLIG KOD
"""
from plugins.base_plugin import BaseGenerator
import os
from jinja2 import Template

class CSSGenerator(BaseGenerator):
    @property
    def name(self):
        return "css_generator"
    
    @property
    def output_format(self):
        return "css"
    
    def generate(self, extraction_data, output_path=None):
        """Generate CSS variables from extraction data"""
        
        # TODO: FLYTTA BEFINTLIG CSS GENERATION LOGIK
        
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'styles.jinja2')
        with open(template_path, 'r') as f:
            template = Template(f.read())
        
        css_content = template.render(**extraction_data)
        
        if output_path:
            css_path = os.path.join(output_path, 'styles.css')
            with open(css_path, 'w') as f:
                f.write(css_content)
            return {'file': css_path}
        
        return {'content': css_content}

def get_generator():
    return CSSGenerator()
```

**CSS Template** (`plugins/generators/css_generator/templates/styles.jinja2`):
```css
/* Generated CSS Variables */
:root {
    /* Colors */
    {% if color_extractor and color_extractor.colors %}
    {% for color in color_extractor.colors[:10] %}
    --color-{{ loop.index }}: {{ color }};
    {% endfor %}
    {% endif %}
    
    /* Fonts */
    {% if font_extractor and font_extractor.fonts %}
    {% for font in font_extractor.fonts[:5] %}
    --font-{{ loop.index }}: '{{ font }}', sans-serif;
    {% endfor %}
    {% endif %}
}

/* Utility Classes */
{% if color_extractor and color_extractor.colors %}
{% for color in color_extractor.colors[:5] %}
.color-{{ loop.index }} {
    color: var(--color-{{ loop.index }});
}

.bg-color-{{ loop.index }} {
    background-color: var(--color-{{ loop.index }});
}
{% endfor %}
{% endif %}
```

### 4. Lägg till BookStack Generator Plugin (20 min)

**BookStack Plugin** (`plugins/generators/bookstack_generator/plugin.py`):
```python
"""
BookStack CSS theme generator plugin
"""
from plugins.base_plugin import BaseGenerator
import os
from jinja2 import Template
import requests
from PIL import Image

class BookStackGenerator(BaseGenerator):
    @property
    def name(self):
        return "bookstack_generator"
    
    @property
    def output_format(self):
        return "bookstack"
    
    def generate(self, extraction_data, output_path=None):
        """Generate complete BookStack template package"""
        
        if not output_path:
            return {'error': 'Output path required for BookStack generator'}
        
        # Create BookStack template directory
        bookstack_dir = os.path.join(output_path, 'bookstack_template')
        assets_dir = os.path.join(bookstack_dir, 'assets')
        os.makedirs(assets_dir, exist_ok=True)
        
        results = {}
        
        # Generate CSS theme
        css_content = self._generate_css_theme(extraction_data)
        css_path = os.path.join(bookstack_dir, 'custom.css')
        with open(css_path, 'w') as f:
            f.write(css_content)
        results['css_file'] = css_path
        
        # Download and process branding assets
        if 'branding_extractor' in extraction_data:
            branding = extraction_data['branding_extractor']
            assets = self._process_branding_assets(branding, assets_dir)
            results['assets'] = assets
        
        # Generate installation guide
        guide_path = self._generate_installation_guide(bookstack_dir, extraction_data)
        results['installation_guide'] = guide_path
        
        return results
    
    def _generate_css_theme(self, data):
        """Generate BookStack CSS using Jinja2 template"""
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'bookstack.css.jinja2')
        with open(template_path, 'r') as f:
            template = Template(f.read())
        
        return template.render(**data)
    
    def _process_branding_assets(self, branding_data, assets_dir):
        """Download and optimize branding assets"""
        assets = {}
        
        # Download logo if available
        if 'logo_url' in branding_data:
            logo_path = self._download_and_optimize_image(
                branding_data['logo_url'], 
                assets_dir, 
                'logo', 
                (200, 60)  # BookStack header logo size
            )
            if logo_path:
                assets['logo'] = logo_path
        
        # Download favicon if available
        if 'favicon_url' in branding_data:
            favicon_path = self._download_and_optimize_image(
                branding_data['favicon_url'],
                assets_dir,
                'favicon',
                (32, 32)
            )
            if favicon_path:
                assets['favicon'] = favicon_path
        
        return assets
    
    def _download_and_optimize_image(self, url, output_dir, name, size):
        """Download and optimize image for BookStack"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Determine file extension
            ext = 'png'  # Default to PNG for better quality
            if '.ico' in url.lower():
                ext = 'ico'
            elif '.svg' in url.lower():
                ext = 'svg'
            
            filename = f"{name}.{ext}"
            filepath = os.path.join(output_dir, filename)
            
            if ext == 'svg':
                # Save SVG as-is
                with open(filepath, 'wb') as f:
                    f.write(response.content)
            else:
                # Process raster images
                with Image.open(io.BytesIO(response.content)) as img:
                    # Convert to RGBA for transparency support
                    img = img.convert('RGBA')
                    
                    # Resize to target size
                    img.thumbnail(size, Image.Resampling.LANCZOS)
                    
                    # Save optimized image
                    img.save(filepath, 'PNG', optimize=True)
            
            return filepath
            
        except Exception as e:
            print(f"Could not process {name} from {url}: {e}")
            return None
    
    def _generate_installation_guide(self, output_dir, data):
        """Generate BookStack installation guide"""
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'installation.md.jinja2')
        with open(template_path, 'r') as f:
            template = Template(f.read())
        
        guide_content = template.render(**data)
        guide_path = os.path.join(output_dir, 'README.md')
        
        with open(guide_path, 'w') as f:
            f.write(guide_content)
        
        return guide_path

def get_generator():
    return BookStackGenerator()
```

**BookStack CSS Template** (`plugins/generators/bookstack_generator/templates/bookstack.css.jinja2`):
```css
/* BookStack Custom Theme - Generated by Web Style Extractor */

:root {
    /* Primary Brand Colors */
    {% if color_extractor and color_extractor.colors %}
    --color-primary: {{ color_extractor.colors[0] if color_extractor.colors else '#0066cc' }};
    --color-primary-light: {{ color_extractor.colors[1] if color_extractor.colors|length > 1 else '#3388dd' }};
    --color-primary-dark: {{ color_extractor.colors[2] if color_extractor.colors|length > 2 else '#004499' }};
    --color-accent: {{ color_extractor.colors[3] if color_extractor.colors|length > 3 else '#ff6b35' }};
    {% else %}
    --color-primary: #0066cc;
    --color-primary-light: #3388dd;
    --color-primary-dark: #004499;
    --color-accent: #ff6b35;
    {% endif %}
    
    /* Typography */
    {% if font_extractor and font_extractor.fonts %}
    --font-heading: '{{ font_extractor.fonts[0] if font_extractor.fonts else 'system-ui' }}', system-ui, sans-serif;
    --font-body: '{{ font_extractor.fonts[1] if font_extractor.fonts|length > 1 else 'system-ui' }}', system-ui, sans-serif;
    {% else %}
    --font-heading: system-ui, sans-serif;
    --font-body: system-ui, sans-serif;
    {% endif %}
    
    /* Layout */
    --header-height: 60px;
    --sidebar-width: 280px;
    --border-radius: 6px;
}

/* ===== BOOKSTACK HEADER ===== */
.header {
    background: var(--color-primary) !important;
    border-bottom: 2px solid var(--color-primary-dark) !important;
}

.header .navbar-brand {
    color: white !important;
    font-family: var(--font-heading) !important;
    font-weight: 600 !important;
}

.header .navbar-nav .nav-link {
    color: rgba(255, 255, 255, 0.9) !important;
    font-family: var(--font-body) !important;
}

.header .navbar-nav .nav-link:hover {
    color: white !important;
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: var(--border-radius) !important;
}

/* ===== BOOKSTACK SIDEBAR ===== */
.sidebar {
    border-right: 1px solid var(--color-primary-light) !important;
    background: #fafafa !important;
}

.sidebar .book-tree a {
    font-family: var(--font-body) !important;
    color: #333 !important;
    border-radius: var(--border-radius) !important;
    transition: all 0.2s ease !important;
}

.sidebar .book-tree a:hover {
    background: var(--color-primary-light) !important;
    color: white !important;
    text-decoration: none !important;
}

.sidebar .book-tree .selected {
    background: var(--color-primary) !important;
    color: white !important;
}

/* ===== BOOKSTACK CONTENT ===== */
.page-content h1, .page-content h2, .page-content h3,
.page-content h4, .page-content h5, .page-content h6 {
    font-family: var(--font-heading) !important;
    color: var(--color-primary-dark) !important;
}

.page-content h1 {
    border-bottom: 3px solid var(--color-primary) !important;
    padding-bottom: 10px !important;
}

.page-content h2 {
    border-bottom: 2px solid var(--color-primary-light) !important;
    padding-bottom: 8px !important;
}

/* ===== BOOKSTACK BUTTONS ===== */
.button-primary, .btn-primary {
    background: var(--color-primary) !important;
    border-color: var(--color-primary) !important;
    border-radius: var(--border-radius) !important;
    font-family: var(--font-body) !important;
    transition: all 0.2s ease !important;
}

.button-primary:hover, .btn-primary:hover {
    background: var(--color-primary-dark) !important;
    border-color: var(--color-primary-dark) !important;
    transform: translateY(-1px) !important;
}

.button-secondary, .btn-secondary {
    background: var(--color-accent) !important;
    border-color: var(--color-accent) !important;
    border-radius: var(--border-radius) !important;
}

/* ===== BOOKSTACK CARDS & PANELS ===== */
.card, .panel {
    border-radius: var(--border-radius) !important;
    border: 1px solid var(--color-primary-light) !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}

.card-header, .panel-heading {
    background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light)) !important;
    color: white !important;
    font-family: var(--font-heading) !important;
    border-radius: var(--border-radius) var(--border-radius) 0 0 !important;
}

/* ===== BOOKSTACK TABLES ===== */
.table th {
    background: var(--color-primary) !important;
    color: white !important;
    font-family: var(--font-heading) !important;
    border: none !important;
}

.table td {
    font-family: var(--font-body) !important;
}

.table-striped tbody tr:nth-of-type(odd) {
    background: rgba(0, 102, 204, 0.05) !important;
}

/* ===== CUSTOM LOGO INTEGRATION ===== */
{% if branding_extractor and branding_extractor.logo_url %}
.header .navbar-brand::before {
    content: '';
    background-image: url('assets/logo.png');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    width: 32px;
    height: 32px;
    display: inline-block;
    margin-right: 12px;
    vertical-align: middle;
}
{% endif %}

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 768px) {
    .sidebar {
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    
    .sidebar.show {
        transform: translateX(0);
    }
    
    .header .navbar-brand {
        font-size: 1rem !important;
    }
}

/* ===== DARK MODE SUPPORT ===== */
@media (prefers-color-scheme: dark) {
    :root {
        --color-primary: {{ color_extractor.colors[0] if color_extractor and color_extractor.colors else '#4a9eff' }};
        --color-primary-light: #66b3ff;
        --color-primary-dark: #2d85e8;
    }
    
    .sidebar {
        background: #2a2a2a !important;
    }
    
    .page-content {
        background: #1a1a1a !important;
        color: #e0e0e0 !important;
    }
}
```

**BookStack Installation Guide Template** (`plugins/generators/bookstack_generator/templates/installation.md.jinja2`):
```markdown
# BookStack Theme Installation Guide

## 🎨 Custom Theme Generated from Website Analysis

This BookStack theme was automatically generated by analyzing the design system of your website.

### 📊 Extracted Design Elements

**Colors Found:**
{% if color_extractor and color_extractor.colors %}
{% for color in color_extractor.colors[:8] %}
- **Color {{ loop.index }}**: `{{ color }}`
{% endfor %}
{% else %}
- No colors detected - using default theme colors
{% endif %}

**Typography:**
{% if font_extractor and font_extractor.fonts %}
{% for font in font_extractor.fonts[:5] %}
- **Font {{ loop.index }}**: {{ font }}
{% endfor %}
{% else %}
- No custom fonts detected - using system fonts
{% endif %}

**Branding Assets:**
{% if branding_extractor %}
- Logo: {% if branding_extractor.logo_url %}✅ Detected and downloaded{% else %}❌ Not found{% endif %}
- Favicon: {% if branding_extractor.favicon_url %}✅ Detected and downloaded{% else %}❌ Not found{% endif %}
{% else %}
- ❌ No branding assets detected
{% endif %}

---

## 🚀 Installation Steps

### 1. Upload Theme Files

Copy the generated files to your BookStack installation:

```bash
# Copy CSS theme
cp custom.css /path/to/bookstack/themes/custom/

# Copy assets (if any)
cp -r assets/ /path/to/bookstack/public/themes/custom/
```

### 2. Configure BookStack

Add to your BookStack `.env` file:

```env
# Enable custom theme
APP_THEME=custom

# Optional: Custom app name
APP_NAME="Your Organization"
```

### 3. Apply Theme

In your BookStack settings:

1. Go to **Settings** → **Customization**
2. **Custom HTML Head Content**, add:

```html
<link rel="stylesheet" href="/themes/custom/custom.css">
```

3. Save settings

### 4. Restart BookStack

```bash
# Clear cache and restart
php artisan cache:clear
php artisan config:clear
sudo systemctl restart apache2  # or nginx
```

---

## 🎯 Customization Options

### Colors
The theme uses CSS custom properties. Override any color by adding to your CSS:

```css
:root {
    --color-primary: #your-color;
    --color-primary-light: #your-light-color;
    --color-primary-dark: #your-dark-color;
}
```

### Typography
Change fonts by modifying:

```css
:root {
    --font-heading: 'Your Font', sans-serif;
    --font-body: 'Your Body Font', sans-serif;
}
```

### Logo
{% if branding_extractor and branding_extractor.logo_url %}
Your logo is automatically integrated in the header. To adjust:

```css
.header .navbar-brand::before {
    width: 40px;  /* Adjust size */
    height: 40px;
}
```
{% else %}
To add your logo, place `logo.png` in `/assets/` and it will automatically appear in the header.
{% endif %}

---

## 🔧 Troubleshooting

**Theme not loading?**
- Check file permissions: `chmod 644 custom.css`
- Verify path: `/themes/custom/custom.css`
- Clear browser cache

**Colors not showing?**
- Check CSS syntax in custom.css
- Verify CSS is loading in browser dev tools

**Logo not appearing?**
- Ensure logo.png exists in `/themes/custom/assets/`
- Check image format (PNG, JPG, SVG supported)

---

## 📝 Generated Information

- **Generated on**: {{ metadata.timestamp if metadata else 'Unknown' }}
- **Source website**: {{ metadata.url if metadata else 'Unknown' }}
- **Generator version**: Web Style Extractor v2.0
- **Theme compatibility**: BookStack v22.0+

---

## 💡 Need Help?

- [BookStack Documentation](https://www.bookstackapp.com/docs/)
- [Customization Guide](https://www.bookstackapp.com/docs/admin/settings/)
- [Web Style Extractor GitHub](https://github.com/your-repo/web-style-extractor)

Enjoy your custom BookStack theme! 🎉
```

### 5. Lägg till Branding Extractor Plugin (15 min)

**Branding Extractor** (`plugins/extractors/branding_extractor/plugin.py`):
```python
"""
Branding and logo extraction plugin för BookStack themes
"""
from plugins.base_plugin import BaseExtractor
import requests
from urllib.parse import urljoin, urlparse

class BrandingExtractor(BaseExtractor):
    @property
    def name(self):
        return "branding_extractor"
    
    @property
    def description(self):
        return "Extracts logos, favicons, and brand elements for theme generation"
    
    def extract(self, soup, driver, url):
        """Extract branding assets and information"""
        branding = {}
        
        # Extract logo
        logo_url = self._extract_logo(soup, url)
        if logo_url:
            branding['logo_url'] = logo_url
        
        # Extract favicon
        favicon_url = self._extract_favicon(soup, url)
        if favicon_url:
            branding['favicon_url'] = favicon_url
        
        # Extract brand colors from meta/CSS
        brand_colors = self._extract_brand_colors(soup)
        if brand_colors:
            branding['brand_colors'] = brand_colors
        
        # Extract organization name
        org_name = self._extract_organization_name(soup)
        if org_name:
            branding['organization'] = org_name
        
        return branding
    
    def _extract_logo(self, soup, base_url):
        """Extract organization logo using various selectors"""
        logo_selectors = [
            'img[class*="logo"]',
            'img[id*="logo"]', 
            'img[alt*="logo"]',
            '.header img',
            '.navbar img',
            '.brand img',
            '.logo img',
            'img[src*="logo"]',
            'header img:first-of-type',
            '.navbar-brand img'
        ]
        
        for selector in logo_selectors:
            logo = soup.select_one(selector)
            if logo and logo.get('src'):
                logo_url = urljoin(base_url, logo['src'])
                
                # Validate it looks like a logo (not a random image)
                if self._is_likely_logo(logo, logo_url):
                    return logo_url
        
        return None
    
    def _extract_favicon(self, soup, base_url):
        """Extract favicon"""
        favicon_selectors = [
            'link[rel="icon"]',
            'link[rel="shortcut icon"]', 
            'link[rel="apple-touch-icon"]',
            'link[rel="favicon"]'
        ]
        
        for selector in favicon_selectors:
            favicon = soup.select_one(selector)
            if favicon and favicon.get('href'):
                return urljoin(base_url, favicon['href'])
        
        # Fallback to default favicon location
        return urljoin(base_url, '/favicon.ico')
    
    def _extract_brand_colors(self, soup):
        """Extract brand colors from CSS custom properties"""
        brand_colors = []
        
        # Look for CSS custom properties that might be brand colors
        style_tags = soup.find_all('style')
        for style in style_tags:
            if style.string:
                lines = style.string.split('\n')
                for line in lines:
                    if '--' in line and ('color' in line.lower() or 'brand' in line.lower()):
                        # Extract color value
                        if ':' in line:
                            color_value = line.split(':')[1].strip().rstrip(';')
                            if color_value.startswith('#') or color_value.startswith('rgb'):
                                brand_colors.append(color_value)
        
        return brand_colors[:5]  # Limit to 5 colors
    
    def _extract_organization_name(self, soup):
        """Extract organization/company name"""
        # Try multiple sources for organization name
        sources = [
            soup.find('meta', {'property': 'og:site_name'}),
            soup.find('meta', {'name': 'application-name'}),
            soup.find('meta', {'name': 'apple-mobile-web-app-title'}),
            soup.title
        ]
        
        for source in sources:
            if source:
                if hasattr(source, 'get'):
                    name = source.get('content')
                else:
                    name = source.string
                
                if name and len(name.strip()) > 0:
                    return name.strip()
        
        return None
    
    def _is_likely_logo(self, img_element, img_url):
        """Heuristic to determine if image is likely a logo"""
        # Check image attributes
        attrs_text = ' '.join([
            str(img_element.get('class', [])),
            str(img_element.get('id', '')),
            str(img_element.get('alt', '')),
            str(img_element.get('src', ''))
        ]).lower()
        
        logo_indicators = ['logo', 'brand', 'header']
        non_logo_indicators = ['banner', 'hero', 'background', 'icon-small']
        
        # Positive indicators
        logo_score = sum(1 for indicator in logo_indicators if indicator in attrs_text)
        
        # Negative indicators  
        non_logo_score = sum(1 for indicator in non_logo_indicators if indicator in attrs_text)
        
        # URL-based heuristics
        url_lower = img_url.lower()
        if any(x in url_lower for x in ['logo', 'brand']):
            logo_score += 2
        
        if any(x in url_lower for x in ['banner', 'hero', 'bg']):
            non_logo_score += 1
        
        return logo_score > non_logo_score

def get_extractor():
    return BrandingExtractor()
```

### 6. Lägg till GitHub Pages Generator (20 min)

**GitHub Pages Generator** (`plugins/generators/github_pages_generator/plugin.py`):
```python
"""
GitHub Pages generator för WEB STYLE EXTRACTOR PROJECT (inte extracted sites)
"""
from plugins.base_plugin import BaseGenerator
import os
from jinja2 import Template
import json
from datetime import datetime

class GitHubPagesGenerator(BaseGenerator):
    @property
    def name(self):
        return "github_pages_generator"
    
    @property
    def output_format(self):
        return "github_pages"
    
    def generate(self, extraction_data, output_path=None):
        """Generate GitHub Pages site för Web Style Extractor PROJECT"""
        
        if not output_path:
            return {'error': 'Output path required for GitHub Pages generator'}
        
        # Create GitHub Pages directory
        pages_dir = os.path.join(output_path, 'github_pages')
        assets_dir = os.path.join(pages_dir, 'assets')
        workflows_dir = os.path.join(pages_dir, '.github', 'workflows')
        
        os.makedirs(assets_dir, exist_ok=True)
        os.makedirs(workflows_dir, exist_ok=True)
        
        results = {}
        
        # Generate landing page
        index_path = self._generate_index_page(pages_dir, extraction_data)
        results['index'] = index_path
        
        # Generate demo page
        demo_path = self._generate_demo_page(pages_dir, extraction_data)
        results['demo'] = demo_path
        
        # Generate examples showcase
        examples_path = self._generate_examples_page(pages_dir, extraction_data)
        results['examples'] = examples_path
        
        # Generate documentation
        docs_path = self._generate_docs_page(pages_dir, extraction_data)
        results['docs'] = docs_path
        
        # Generate assets
        css_path = self._generate_styles(assets_dir)
        js_path = self._generate_javascript(assets_dir)
        results['assets'] = {'css': css_path, 'js': js_path}
        
        # Generate GitHub workflow
        workflow_path = self._generate_github_workflow(workflows_dir)
        results['workflow'] = workflow_path
        
        return results
    
    def _generate_index_page(self, output_dir, data):
        """Generate project landing page"""
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html.jinja2')
        with open(template_path, 'r') as f:
            template = Template(f.read())
        
        html_content = template.render(
            project_name="Web Style Extractor",
            description="Extract colors, fonts, and design systems from any website",
            data=data,
            generated_at=datetime.now().isoformat()
        )
        
        index_path = os.path.join(output_dir, 'index.html')
        with open(index_path, 'w') as f:
            f.write(html_content)
        
        return index_path
    
    def _generate_demo_page(self, output_dir, data):
        """Generate interactive demo page"""
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'demo.html.jinja2')
        with open(template_path, 'r') as f:
            template = Template(f.read())
        
        html_content = template.render(
            extraction_data=data,
            available_formats=['json', 'css', 'mediawiki', 'tailwind', 'bookstack']
        )
        
        demo_path = os.path.join(output_dir, 'demo.html')
        with open(demo_path, 'w') as f:
            f.write(html_content)
        
        return demo_path
    
    def _generate_examples_page(self, output_dir, data):
        """Generate examples showcase page"""
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'examples.html.jinja2')
        
        # Load examples from projects directory
        examples_data = self._load_project_examples()
        
        with open(template_path, 'r') as f:
            template = Template(f.read())
        
        html_content = template.render(
            examples=examples_data,
            total_examples=len(examples_data)
        )
        
        examples_path = os.path.join(output_dir, 'examples.html')
        with open(examples_path, 'w') as f:
            f.write(html_content)
        
        return examples_path
    
    def _load_project_examples(self):
        """Load real examples from projects/ directory"""
        examples = []
        projects_dir = 'projects'
        
        if os.path.exists(projects_dir):
            for domain in os.listdir(projects_dir):
                domain_path = os.path.join(projects_dir, domain)
                if os.path.isdir(domain_path) and not domain.startswith('.'):
                    
                    # Load metadata
                    metadata_path = os.path.join(domain_path, 'metadata.txt')
                    metadata = {}
                    if os.path.exists(metadata_path):
                        with open(metadata_path, 'r') as f:
                            for line in f:
                                if ':' in line:
                                    key, value = line.split(':', 1)
                                    metadata[key.strip()] = value.strip()
                    
                    # Load JSON data if available
                    json_path = os.path.join(domain_path, 'styles.json')
                    json_data = {}
                    if os.path.exists(json_path):
                        with open(json_path, 'r') as f:
                            json_data = json.load(f)
                    
                    # Get available formats
                    formats = []
                    for fmt in ['css', 'mediawiki', 'tailwind']:
                        if os.path.exists(os.path.join(domain_path, f'styles.{fmt}')):
                            formats.append(fmt)
                    
                    if os.path.exists(os.path.join(domain_path, 'bookstack_template')):
                        formats.append('bookstack')
                    
                    examples.append({
                        'domain': domain,
                        'metadata': metadata,
                        'data': json_data,
                        'formats': formats
                    })
        
        return examples
    
    def _generate_docs_page(self, output_dir, data):
        """Generate documentation page"""
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'docs.html.jinja2')
        with open(template_path, 'r') as f:
            template = Template(f.read())
        
        html_content = template.render(
            plugins_available=['color_extractor', 'font_extractor', 'css_extractor', 'branding_extractor'],
            generators_available=['json', 'css', 'mediawiki', 'tailwind', 'bookstack']
        )
        
        docs_path = os.path.join(output_dir, 'docs.html')
        with open(docs_path, 'w') as f:
            f.write(html_content)
        
        return docs_path
    
    def _generate_styles(self, assets_dir):
        """Generate CSS for GitHub Pages site"""
        css_content = """
/* Web Style Extractor GitHub Pages Styles */
:root {
    --primary-color: #2563eb;
    --secondary-color: #64748b;
    --accent-color: #f59e0b;
    --bg-color: #ffffff;
    --text-color: #1f2937;
    --border-color: #e5e7eb;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: system-ui, -apple-system, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background: var(--bg-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

/* Header */
.header {
    background: linear-gradient(135deg, var(--primary-color), #1e40af);
    color: white;
    padding: 2rem 0;
    text-align: center;
}

.header h1 {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.header p {
    font-size: 1.2rem;
    opacity: 0.9;
}

/* Navigation */
.nav {
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-container {
    display: flex;
    justify-content: center;
    padding: 1rem;
}

.nav a {
    color: var(--text-color);
    text-decoration: none;
    padding: 0.5rem 1rem;
    margin: 0 0.5rem;
    border-radius: 6px;
    transition: all 0.2s ease;
}

.nav a:hover,
.nav a.active {
    background: var(--primary-color);
    color: white;
}

/* Main Content */
.main {
    padding: 3rem 0;
}

.section {
    margin-bottom: 4rem;
}

.section h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: var(--primary-color);
}

/* Feature Grid */
.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.feature {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.2s ease;
}

.feature:hover {
    transform: translateY(-4px);
}

.feature h3 {
    color: var(--primary-color);
    margin-bottom: 1rem;
}

/* Examples Grid */
.examples-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.example {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.example-header {
    background: var(--primary-color);
    color: white;
    padding: 1rem;
    font-weight: 600;
}

.example-content {
    padding: 1.5rem;
}

.color-palette {
    display: flex;
    gap: 0.5rem;
    margin: 1rem 0;
    flex-wrap: wrap;
}

.color-swatch {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    border: 2px solid var(--border-color);
    position: relative;
    cursor: pointer;
}

.color-swatch:hover::after {
    content: attr(data-color);
    position: absolute;
    top: -30px;
    left: 50%;
    transform: translateX(-50%);
    background: #333;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    white-space: nowrap;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background: var(--primary-color);
    color: white;
    text-decoration: none;
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.2s ease;
    border: none;
    cursor: pointer;
}

.btn:hover {
    background: #1d4ed8;
    transform: translateY(-2px);
}

.btn-secondary {
    background: var(--secondary-color);
}

.btn-secondary:hover {
    background: #475569;
}

/* Code Blocks */
pre {
    background: #1f2937;
    color: #f9fafb;
    padding: 1rem;
    border-radius: 8px;
    overflow-x: auto;
    margin: 1rem 0;
}

/* Footer */
.footer {
    background: var(--text-color);
    color: white;
    text-align: center;
    padding: 2rem 0;
    margin-top: 4rem;
}

/* Responsive */
@media (max-width: 768px) {
    .header h1 {
        font-size: 2rem;
    }
    
    .nav-container {
        flex-direction: column;
    }
    
    .examples-grid {
        grid-template-columns: 1fr;
    }
}
"""
        
        css_path = os.path.join(assets_dir, 'styles.css')
        with open(css_path, 'w') as f:
            f.write(css_content)
        
        return css_path
    
    def _generate_javascript(self, assets_dir):
        """Generate JavaScript for interactive features"""
        js_content = """
// Web Style Extractor GitHub Pages JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initNavigation();
    initColorPalettes();
    initDemoFeatures();
});

function initNavigation() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Active navigation highlighting
    const navLinks = document.querySelectorAll('.nav a');
    const sections = document.querySelectorAll('.section');
    
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= sectionTop - 60) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

function initColorPalettes() {
    // Add click-to-copy functionality for color swatches
    document.querySelectorAll('.color-swatch').forEach(swatch => {
        swatch.addEventListener('click', function() {
            const color = this.dataset.color;
            if (color) {
                copyToClipboard(color);
                showToast(`Copied ${color} to clipboard!`);
            }
        });
    });
}

function initDemoFeatures() {
    // Live URL extraction demo
    const demoForm = document.getElementById('demo-form');
    if (demoForm)