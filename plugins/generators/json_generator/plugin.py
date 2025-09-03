"""
JSON output generator - generates structured JSON output
"""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from plugins.base_plugin import BaseGenerator
from typing import Dict, Any


class JSONGenerator(BaseGenerator):
    @property
    def name(self):
        return "json_generator"
    
    @property
    def output_format(self):
        return "json"
    
    def generate(self, extraction_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
        """Generate JSON output from extraction data"""
        
        # Create structured JSON output
        output = {
            'metadata': {
                'generated_by': 'Web Style Extractor v2.0',
                'generated_at': datetime.now().isoformat(),
                'extraction_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'url': extraction_data.get('url', ''),
                'version': '2.0.0'
            },
            'extraction_results': self._clean_extraction_data(extraction_data),
            'summary': self._generate_summary(extraction_data)
        }
        
        # Add usage examples
        output['usage_examples'] = self._generate_usage_examples(extraction_data)
        
        if output_path:
            # Create format-specific directory
            format_dir = Path(output_path) / 'json'
            format_dir.mkdir(exist_ok=True)
            
            json_path = format_dir / 'styles.json'
            
            # Archive existing file if it exists
            if json_path.exists():
                self.archive_existing_file(json_path, format_dir)
            
            # Write new file
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            # Create format-specific README
            self._create_format_readme(format_dir, output)
            
            return {'file': str(json_path), 'content': output}
        
        return {'content': output}
    
    def _clean_extraction_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and organize extraction data for JSON output"""
        cleaned = {}
        
        # Process each extractor's results
        for extractor_name, extractor_data in data.get('extraction', {}).items():
            if extractor_data:  # Only include non-empty results
                cleaned[extractor_name] = self._clean_extractor_data(extractor_data)
        
        return cleaned
    
    def _clean_extractor_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean individual extractor data"""
        if not isinstance(data, dict):
            return data
        
        cleaned = {}
        for key, value in data.items():
            # Skip very large text fields but keep reference
            if isinstance(value, str) and len(value) > 5000:
                cleaned[key] = f"[Large text content: {len(value)} characters]"
            elif isinstance(value, list) and len(value) > 50:
                cleaned[key] = value[:50]  # Truncate large lists
                cleaned[f'{key}_total_count'] = len(value)
            else:
                cleaned[key] = value
        
        return cleaned
    
    def _generate_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of extracted data"""
        summary = {}
        
        # Color summary
        if 'color_extractor' in data.get('extraction', {}):
            color_data = data['extraction']['color_extractor']
            summary['colors'] = {
                'total_found': color_data.get('total_colors_found', 0),
                'primary_color': color_data.get('primary_color'),
                'has_palette': bool(color_data.get('color_palette', {}).get('primary'))
            }
        
        # Font summary
        if 'font_extractor' in data.get('extraction', {}):
            font_data = data['extraction']['font_extractor']
            summary['typography'] = {
                'total_fonts': font_data.get('total_fonts_found', 0),
                'primary_font': font_data.get('primary_font'),
                'has_google_fonts': bool(font_data.get('google_fonts', [])),
                'font_categories': list(font_data.get('font_categories', {}).keys())
            }
        
        # HTML summary
        if 'html_extractor' in data.get('extraction', {}):
            html_data = data['extraction']['html_extractor']
            summary['structure'] = {
                'title': html_data.get('title', ''),
                'has_description': bool(html_data.get('meta_description')),
                'total_elements': html_data.get('dom_structure', {}).get('total_elements', 0),
                'semantic_score': len(html_data.get('semantic_elements', {}))
            }
        
        # CSS summary
        if 'css_extractor' in data.get('extraction', {}):
            css_data = data['extraction']['css_extractor']
            summary['styles'] = {
                'total_rules': css_data.get('rule_count', 0),
                'css_size': css_data.get('total_css_size', 0),
                'has_custom_properties': bool(css_data.get('custom_properties', {})),
                'modern_features': list(css_data.get('modern_features', {}).keys())
            }
        
        return summary
    
    def _generate_usage_examples(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate usage examples for the extracted data"""
        examples = {}
        
        # Color usage examples
        if 'color_extractor' in data.get('extraction', {}):
            color_data = data['extraction']['color_extractor']
            colors = color_data.get('colors', [])
            
            if colors:
                examples['colors'] = {
                    'css_variables': {
                        f'--primary-{i+1}': color 
                        for i, color in enumerate(colors[:5])
                    },
                    'tailwind_config': {
                        'primary': {
                            str(i*100 + 100): color 
                            for i, color in enumerate(colors[:9])
                        }
                    },
                    'sass_variables': {
                        f'$primary-{i+1}': color 
                        for i, color in enumerate(colors[:5])
                    }
                }
        
        # Font usage examples
        if 'font_extractor' in data.get('extraction', {}):
            font_data = data['extraction']['font_extractor']
            fonts = font_data.get('fonts', [])
            
            if fonts:
                examples['fonts'] = {
                    'css_font_stack': {
                        '--font-primary': f"'{fonts[0]}', system-ui, sans-serif" if fonts else "",
                        '--font-secondary': f"'{fonts[1]}', system-ui, sans-serif" if len(fonts) > 1 else ""
                    },
                    'google_fonts_import': [
                        f"@import url('https://fonts.googleapis.com/css2?family={font.replace(' ', '+')}');"
                        for font in fonts[:3] if ' ' in font  # Likely web fonts
                    ]
                }
        
        return examples
    
    def _create_format_readme(self, format_dir: Path, output: dict):
        """Create format-specific README with usage instructions"""
        readme_content = f"""# JSON Format Usage

This directory contains the extracted style data in JSON format.

## Files
- `styles.json` - Complete extraction results with colors, fonts, and metadata

## Usage Examples

### JavaScript/Node.js
```javascript
const styleData = require('./styles.json');

// Access colors
const colors = styleData.extraction_results.color_extractor?.colors || [];
console.log('Primary color:', colors[0]);

// Access fonts  
const fonts = styleData.extraction_results.font_extractor?.fonts || [];
console.log('Primary font:', fonts[0]);
```

### Python
```python
import json

with open('styles.json', 'r') as f:
    style_data = json.load(f)

colors = style_data.get('extraction_results', {{}}).get('color_extractor', {{}}).get('colors', [])
fonts = style_data.get('extraction_results', {{}}).get('font_extractor', {{}}).get('fonts', [])

print(f"Found {{len(colors)}} colors and {{len(fonts)}} fonts")
```

### API Integration
Perfect for REST APIs, GraphQL responses, or any system that consumes JSON data.

## Data Structure
```json
{{
  "metadata": {{
    "generated_by": "Web Style Extractor",
    "url": "...",
    "generated_at": "..."
  }},
  "extraction_results": {{
    "color_extractor": {{ "colors": [...] }},
    "font_extractor": {{ "fonts": [...] }},
    "html_extractor": {{ ... }},
    "css_extractor": {{ ... }}
  }},
  "usage_examples": {{ ... }}
}}
```

Generated by Web Style Extractor"""
        
        readme_path = format_dir / 'README.md'
        readme_path.write_text(readme_content, encoding='utf-8')


def get_generator():
    return JSONGenerator()