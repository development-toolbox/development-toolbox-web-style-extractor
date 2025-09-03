"""
MediaWiki Generator Plugin
Generates MediaWiki-formatted documentation with color tables and font information
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any
from plugins.base_plugin import BaseGenerator


class MediaWikiGeneratorPlugin(BaseGenerator):
    """Generates MediaWiki format output"""
    
    @property
    def name(self) -> str:
        return "MediaWiki Generator"
    
    @property
    def output_format(self) -> str:
        return "mediawiki"
    
    @property
    def description(self) -> str:
        return "Ready-to-use MediaWiki template with color tables and font documentation"
    
    @property
    def emoji(self) -> str:
        return "📝"
        
    @property
    def short_description(self) -> str:
        return "MediaWiki template with color tables and font documentation"
        
    @property
    def file_extension(self) -> str:
        return "mediawiki"
    
    @property
    def capabilities(self) -> list:
        return [
            'Color palette tables with visual swatches',
            'Font lists with classifications', 
            'Wiki-formatted documentation',
            'Copy-paste ready templates'
        ]
    
    @property
    def use_cases(self) -> list:
        return [
            'Wiki documentation',
            'Style guides',
            'Design system docs',
            'Team knowledge bases'
        ]
    
    def generate(self, extraction_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
        """Generate MediaWiki format output"""
        try:
            # Get extraction data
            color_data = extraction_data.get('color_extractor', {})
            font_data = extraction_data.get('font_extractor', {})
            html_data = extraction_data.get('html_extractor', {})
            
            url = html_data.get('url', 'Unknown URL')
            
            # Build MediaWiki content
            content = self._generate_mediawiki_content(url, color_data, font_data, html_data)
            
            # Write output file
            if output_path:
                # Create format-specific directory
                format_dir = Path(output_path) / 'mediawiki'
                format_dir.mkdir(exist_ok=True)
                
                # Build file path inside format_dir
                output_file = format_dir / f'styles.{self.file_extension}'
                
                # Check if file exists and archive using base class method
                if output_file.exists():
                    self.archive_existing_file(output_file, format_dir)
                
                # Write new file to format_dir
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Create format-specific README
                self._create_format_readme(format_dir, color_data, font_data)
                
                logging.info(f"✅ MediaWiki documentation generated: {output_file}")
                
                return {
                    'success': True,
                    'file': str(output_file),
                    'format': self.output_format,
                    'content': content
                }
            else:
                return {
                    'success': True, 
                    'format': self.output_format,
                    'content': content
                }
                
        except Exception as e:
            logging.error(f"MediaWiki generation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _generate_mediawiki_content(self, url: str, color_data: dict, font_data: dict, html_data: dict) -> str:
        """Generate the MediaWiki formatted content"""
        
        content = []
        content.append(f"== Style Guide for {url} ==\n")
        
        # Basic information
        body_bg = html_data.get('body_background', 'Not detected')
        body_font = html_data.get('body_font', 'Not detected')
        
        content.append("=== Basic Information ===")
        content.append(f"'''Body Background:''' {body_bg}")
        content.append(f"'''Body Font:''' {body_font}\n")
        
        # Colors section
        colors = color_data.get('colors', [])
        if colors:
            content.append("=== Color Palette ===")
            content.append('{| class="wikitable"')
            content.append("|-")
            content.append("! Color !! Value !! Usage")
            
            for i, color in enumerate(colors[:10]):  # Limit to first 10 colors
                usage = f"Color {i+1}"
                content.append("|-")
                content.append(f"| style='background-color: {color}' | ")
                content.append(f"| <code>{color}</code>")
                content.append(f"| {usage}")
            
            content.append("|}")
            content.append("")
        
        # Fonts section  
        fonts = font_data.get('fonts', [])
        if fonts:
            content.append("=== Typography ===")
            content.append('{| class="wikitable"')
            content.append("|-")
            content.append("! Font Family !! Type")
            
            for font in fonts[:8]:  # Limit to first 8 fonts
                font_type = self._classify_font(font)
                content.append("|-")
                content.append(f"| {font}")
                content.append(f"| {font_type}")
            
            content.append("|}")
            content.append("")
        
        # Usage instructions
        content.append("=== How to Use ===")
        content.append("# Copy the color values from the table above")
        content.append("# Use the font families in your CSS or theme settings") 
        content.append("# Apply the body background color to match the original site")
        content.append("# Test the color combinations for accessibility")
        
        return "\n".join(content)
    
    def _classify_font(self, font: str) -> str:
        """Classify a font family"""
        font_lower = font.lower()
        
        if any(keyword in font_lower for keyword in ['mono', 'code', 'console', 'courier']):
            return "Monospace"
        elif any(keyword in font_lower for keyword in ['serif', 'times', 'georgia']):
            return "Serif"
        elif any(keyword in font_lower for keyword in ['display', 'heading', 'title']):
            return "Display"
        else:
            return "Sans-serif"
    
    def _create_format_readme(self, format_dir: Path, color_data: dict, font_data: dict):
        """Create format-specific README with usage instructions"""
        readme_content = f"""# MediaWiki Format Usage

This directory contains the extracted styles in MediaWiki format.

## Files
- `styles.mediawiki` - Complete style guide with color tables and typography in MediaWiki format

## Usage in MediaWiki

### 1. Direct Copy-Paste
The generated MediaWiki content can be copied directly into any MediaWiki page:

```
1. Edit a page in your MediaWiki installation
2. Switch to source editing mode
3. Copy the entire content from styles.mediawiki
4. Paste into your wiki page
5. Save the page
```

### 2. Create a Template
Create a reusable template for consistent styling across pages:

```mediawiki
<!-- Create Template:StyleGuide -->
{{{{subst:Template:StyleGuide}}}}

<!-- Then use in any page -->
{{{{StyleGuide}}}}
```

## MediaWiki Syntax Features

### Color Tables
The generated color tables use MediaWiki's wikitable class:

```mediawiki
{{| class="wikitable"
|-
! Color !! Value !! Usage
|-
| style='background-color: #ff0000' | 
| <code>#ff0000</code>
| Primary Red
|}}
```

### Typography Tables
Font information is formatted as structured tables:

```mediawiki
{{| class="wikitable"
|-
! Font Family !! Type
|-
| Arial, sans-serif
| Sans-serif
|}}
```

## Integration Examples

### Style Guide Page
Create a dedicated style guide page:

```mediawiki
= Brand Style Guide =

== Overview ==
This page contains the visual style guidelines for our brand.

{{{{subst:styles.mediawiki}}}}

== Usage Guidelines ==
* Always use primary colors for headings
* Secondary colors for backgrounds
* Follow font hierarchy for consistency
```

### Component Documentation
Document UI components with extracted styles:

```mediawiki
= Button Component =

== Variants ==
* '''Primary:''' Background: <code>{{{{color:primary}}}}</code>
* '''Secondary:''' Background: <code>{{{{color:secondary}}}}</code>
* '''Font:''' {{{{font:primary}}}}

== Examples ==
<div style="background: #ff0000; color: white; padding: 8px;">Primary Button</div>
```

### Theme Documentation
Document website themes and variations:

```mediawiki
= Theme Variations =

== Light Theme ==
{{| class="wikitable"
|-
! Element !! Color !! Usage
|-
| Background
| <code>#ffffff</code>
| Main background
|-
| Text
| <code>#333333</code>
| Primary text color
|}}
```

## Advanced Usage

### Custom CSS Integration
Combine with MediaWiki's custom CSS:

```css
/* MediaWiki:Common.css */
.brand-primary {{
    background-color: {color_data.get('colors', ['#000000'])[0] if color_data.get('colors') else '#000000'};
    color: white;
}}

.brand-font {{
    font-family: {font_data.get('fonts', ['Arial'])[0] if font_data.get('fonts') else 'Arial'}, sans-serif;
}}
```

### Template Variables
Create template variables for consistent usage:

```mediawiki
<!-- Template:Colors -->
<includeonly>
{{{{#switch: {{{{1}}}}
  | primary = {color_data.get('colors', ['#000000'])[0] if color_data.get('colors') else '#000000'}
  | secondary = {color_data.get('colors', ['#000000'])[1] if len(color_data.get('colors', [])) > 1 else '#666666'}
  | #default = #000000
}}}}
</includeonly>

<!-- Usage: {{{{Colors|primary}}}} -->
```

### Semantic Markup
Use semantic HTML within MediaWiki:

```mediawiki
<div class="style-guide">
  <section class="color-palette">
    <h2>Color Palette</h2>
    <!-- Color table content -->
  </section>
  
  <section class="typography">
    <h2>Typography</h2>
    <!-- Font table content -->
  </section>
</div>
```

## Export and Sharing

### Export Options
- **PDF Export:** Use MediaWiki's PDF export feature
- **Print Version:** Create print-friendly versions
- **Mobile View:** Optimize for mobile MediaWiki views

### Collaboration
- **Discussion Pages:** Use talk pages for style discussions
- **Version History:** Track style guide changes over time
- **User Permissions:** Control who can edit style documentation

Generated by Web Style Extractor"""
        
        readme_path = format_dir / 'README.md'
        readme_path.write_text(readme_content, encoding='utf-8')


def get_generator():
    return MediaWikiGeneratorPlugin()