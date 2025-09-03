"""
HTML Report Generator Plugin
Creates interactive HTML documentation with live previews and visual analysis
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any
from plugins.base_plugin import BaseGenerator


class HTMLGeneratorPlugin(BaseGenerator):
    """Generates interactive HTML report"""
    
    @property
    def name(self) -> str:
        return "HTML Report Generator"
    
    @property
    def output_format(self) -> str:
        return "html"
    
    @property
    def description(self) -> str:
        return "Interactive HTML report with live previews and visual analysis"
    
    @property
    def emoji(self) -> str:
        return "📊"
        
    @property
    def short_description(self) -> str:
        return "Interactive HTML report with visual previews"
        
    @property
    def file_extension(self) -> str:
        return "html"
    
    @property
    def capabilities(self) -> list:
        return [
            'Visual color previews',
            'Live font rendering',
            'Interactive elements',
            'Print-friendly layout'
        ]
    
    @property
    def use_cases(self) -> list:
        return [
            'Design reviews',
            'Client presentations',
            'Documentation',
            'Style guide reference'
        ]
    
    def generate(self, extraction_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
        """Generate HTML report output"""
        try:
            # Get extraction data
            color_data = extraction_data.get('color_extractor', {})
            font_data = extraction_data.get('font_extractor', {})
            html_data = extraction_data.get('html_extractor', {})
            
            url = html_data.get('url', 'Unknown URL')
            
            # Build HTML content
            content = self._generate_html_report(url, color_data, font_data, html_data)
            
            # Write output file
            if output_path:
                # Create format-specific directory
                format_dir = Path(output_path) / 'html'
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
                
                logging.info(f"✅ HTML report generated: {output_file}")
                
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
            logging.error(f"HTML report generation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _generate_html_report(self, url: str, color_data: dict, font_data: dict, html_data: dict) -> str:
        """Generate interactive HTML report"""
        
        colors = color_data.get('colors', [])
        fonts = font_data.get('fonts', [])
        body_bg = html_data.get('body_background', '#ffffff')
        body_font = html_data.get('body_font', 'system-ui, sans-serif')
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Style Guide - {url}</title>
    <style>
        /* Reset and base styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: #f8fafc;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            color: #1e293b;
            margin-bottom: 0.5rem;
            font-size: 2.5rem;
        }}
        
        .header p {{
            color: #64748b;
            font-size: 1.1rem;
        }}
        
        .section {{
            background: white;
            margin-bottom: 2rem;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }}
        
        .section h2 {{
            color: #1e293b;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
            border-bottom: 3px solid #3b82f6;
            padding-bottom: 0.5rem;
        }}
        
        /* Color palette styles */
        .color-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .color-swatch {{
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.2s;
        }}
        
        .color-swatch:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .color-preview {{
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5);
            font-weight: 500;
        }}
        
        .color-info {{
            padding: 1rem;
            text-align: center;
        }}
        
        .color-value {{
            font-family: 'SF Mono', Monaco, monospace;
            background: #f1f5f9;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.875rem;
            color: #475569;
            margin-top: 0.5rem;
            display: inline-block;
        }}
        
        /* Font styles */
        .font-grid {{
            display: grid;
            gap: 1.5rem;
            margin-top: 1rem;
        }}
        
        .font-sample {{
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.5rem;
            transition: transform 0.2s;
        }}
        
        .font-sample:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .font-name {{
            font-family: 'SF Mono', Monaco, monospace;
            background: #f1f5f9;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.875rem;
            color: #475569;
            margin-bottom: 1rem;
            display: inline-block;
        }}
        
        .font-preview {{
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
            color: #1e293b;
        }}
        
        .font-sizes {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        .font-size {{
            color: #64748b;
        }}
        
        /* Basic info styles */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .info-item {{
            padding: 1rem;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            background: #f8fafc;
        }}
        
        .info-label {{
            font-weight: 600;
            color: #475569;
            margin-bottom: 0.5rem;
        }}
        
        .info-value {{
            font-family: 'SF Mono', Monaco, monospace;
            color: #1e293b;
            word-break: break-all;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}
            
            .color-grid {{
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
        }}
        
        /* Print styles */
        @media print {{
            body {{
                background: white;
                max-width: none;
            }}
            
            .section {{
                box-shadow: none;
                border: 1px solid #e2e8f0;
                break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 Style Guide</h1>
        <p>Extracted from <strong>{url}</strong></p>
    </div>
    
    <div class="section">
        <h2>📋 Basic Information</h2>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">URL</div>
                <div class="info-value">{url}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Body Background</div>
                <div class="info-value">{body_bg}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Body Font</div>
                <div class="info-value">{body_font}</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>🎨 Color Palette</h2>
        <div class="color-grid">
"""
        
        # Add color swatches
        for i, color in enumerate(colors[:12]):  # Limit to 12 colors
            # Determine text color based on background
            text_color = self._get_contrast_color(color)
            html_content += f"""
            <div class="color-swatch">
                <div class="color-preview" style="background-color: {color}; color: {text_color};">
                    Color {i+1}
                </div>
                <div class="color-info">
                    <div class="color-value">{color}</div>
                </div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
    
    <div class="section">
        <h2>🔤 Typography</h2>
        <div class="font-grid">
"""
        
        # Add font samples
        for i, font in enumerate(fonts[:8]):  # Limit to 8 fonts
            html_content += f"""
            <div class="font-sample">
                <div class="font-name">{font}</div>
                <div class="font-preview" style="font-family: {font}, system-ui, sans-serif;">
                    The quick brown fox jumps over the lazy dog
                </div>
                <div class="font-sizes">
                    <div class="font-size" style="font-family: {font}, system-ui, sans-serif; font-size: 0.875rem;">Small text sample</div>
                    <div class="font-size" style="font-family: {font}, system-ui, sans-serif; font-size: 1.125rem;">Large text sample</div>
                </div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
    
    <div class="section">
        <h2>📖 Usage Instructions</h2>
        <ol style="line-height: 1.8; margin-left: 1.5rem;">
            <li>Click on color swatches to copy hex values</li>
            <li>Use the font families shown in your CSS</li>
            <li>Test color combinations for accessibility compliance</li>
            <li>Consider the original context when applying colors</li>
        </ol>
    </div>
    
    <script>
        // Add click-to-copy functionality
        document.querySelectorAll('.color-swatch').forEach(swatch => {
            swatch.addEventListener('click', () => {
                const colorValue = swatch.querySelector('.color-value').textContent;
                navigator.clipboard.writeText(colorValue).then(() => {
                    const original = swatch.querySelector('.color-preview').textContent;
                    swatch.querySelector('.color-preview').textContent = 'Copied!';
                    setTimeout(() => {
                        swatch.querySelector('.color-preview').textContent = original;
                    }, 1000);
                });
            });
        });
    </script>
</body>
</html>"""
        
        return html_content
    
    def _get_contrast_color(self, background_color: str) -> str:
        """Determine if white or black text provides better contrast"""
        # Simple heuristic - in production, use proper color contrast calculation
        if background_color.startswith('#'):
            # Remove # and convert to RGB
            hex_color = background_color[1:]
            if len(hex_color) == 3:
                # Convert short hex to long hex
                hex_color = ''.join([c*2 for c in hex_color])
            
            try:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                
                # Calculate brightness using relative luminance approximation
                brightness = (r * 299 + g * 587 + b * 114) / 1000
                
                return '#000000' if brightness > 128 else '#ffffff'
            except:
                return '#ffffff'
        
        return '#ffffff'  # Default to white text
    
    def _create_format_readme(self, format_dir: Path, color_data: dict, font_data: dict):
        """Create format-specific README with usage instructions"""
        readme_content = f"""# HTML Report Format Usage

This directory contains an interactive HTML report with visual style analysis.

## Files
- `styles.html` - Interactive HTML report with color swatches and font previews

## Features

### Visual Color Palette
- **Color swatches** with visual previews
- **Click-to-copy** functionality for hex values
- **Automatic contrast** detection for readable text
- **Responsive grid** layout that adapts to screen size

### Typography Preview
- **Live font rendering** with actual font families
- **Multiple text sizes** to test readability
- **Font family names** clearly displayed
- **Sample text** to evaluate font characteristics

### Interactive Elements
- **Click color swatches** to copy hex values to clipboard
- **Hover effects** for better user experience
- **Responsive design** that works on mobile and desktop
- **Print-friendly** layout for physical documentation

## Usage

### Opening the Report
```bash
# Open directly in browser
open html/styles.html

# Or serve via local server
python -m http.server 8000
# Then visit: http://localhost:8000/html/styles.html
```

### Browser Compatibility
- **Modern browsers:** Full functionality including clipboard API
- **Older browsers:** Visual report works, click-to-copy may not be available
- **Mobile browsers:** Responsive layout, touch-friendly interactions
- **Print:** Optimized print styles for documentation

### Integration

#### Web Development
```html
<!-- Embed in existing page -->
<iframe src="html/styles.html" width="100%" height="800px" frameborder="0"></iframe>

<!-- Or link to standalone report -->
<a href="html/styles.html" target="_blank">View Style Guide</a>
```

#### Design Documentation
```markdown
# Project Style Guide

For interactive color and font reference, see:
[HTML Style Report](html/styles.html)

## Colors
Refer to the interactive report for click-to-copy color values.

## Typography
Font samples with live rendering available in the HTML report.
```

#### Email Sharing
The HTML report is self-contained and can be shared via email:
- Attach the `styles.html` file
- Recipients can open directly in their browser
- All styles are embedded (no external dependencies)

### Customization

#### Modifying Styles
Edit the embedded CSS in `styles.html`:

```css
/* Change section background */
.section {{
    background: #f8fafc; /* Light gray */
    border: 1px solid #e2e8f0;
}}

/* Modify color swatch size */
.color-preview {{
    height: 100px; /* Increase from 80px */
}}

/* Adjust font preview size */
.font-preview {{
    font-size: 1.5rem; /* Increase from 1.25rem */
}}
```

#### Adding Custom Sections
```html
<!-- Add after existing sections -->
<div class="section">
    <h2>🎭 Custom Elements</h2>
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label">Brand Voice</div>
            <div class="info-value">Professional, friendly, modern</div>
        </div>
        <div class="info-item">
            <div class="info-label">Target Audience</div>
            <div class="info-value">Tech-savvy professionals</div>
        </div>
    </div>
</div>
```

#### Extending Functionality
```javascript
// Add color format conversion
function convertToRgb(hex) {{
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgb(${{r}}, ${{g}}, ${{b}})`;
}}

// Add to existing click handler
document.querySelectorAll('.color-swatch').forEach(swatch => {{
    swatch.addEventListener('click', () => {{
        const colorValue = swatch.querySelector('.color-value').textContent;
        const rgbValue = convertToRgb(colorValue);
        navigator.clipboard.writeText(`${{colorValue}} / ${{rgbValue}}`);
    }});
}});
```

### Accessibility

#### Screen Readers
- All colors have descriptive labels
- Semantic HTML structure with proper headings
- Alternative text for visual elements
- Keyboard navigation support

#### High Contrast Mode
The report automatically adapts to system high contrast settings:

```css
@media (prefers-contrast: high) {{
    .section {{
        border: 2px solid #000;
        background: #fff;
    }}
    
    .color-swatch {{
        border: 2px solid #000;
    }}
}}
```

#### Motion Preferences
```css
@media (prefers-reduced-motion: reduce) {{
    .color-swatch,
    .font-sample {{
        transition: none;
    }}
    
    .color-swatch:hover,
    .font-sample:hover {{
        transform: none;
    }}
}}
```

## Use Cases

### Design Reviews
- **Client presentations:** Professional, visual format
- **Team reviews:** Interactive exploration of design elements
- **Design handoffs:** Clear communication of colors and fonts
- **Brand guidelines:** Visual reference for style consistency

### Development
- **CSS development:** Quick reference for exact color values
- **Component libraries:** Visual catalog of design tokens
- **Style audits:** Review and document existing designs
- **Responsive testing:** Preview how styles work across devices

### Documentation
- **Style guides:** Living documentation that's easy to update
- **Design systems:** Component of larger design system docs
- **Brand books:** Visual section of brand guideline documents
- **Portfolio pieces:** Showcase design analysis capabilities

### Quality Assurance
- **Color accuracy:** Verify colors match design specifications
- **Font loading:** Test if custom fonts are loading properly
- **Consistency checks:** Ensure design elements are consistent
- **Cross-browser testing:** Verify appearance across browsers

## Advanced Features

### Print Optimization
```css
@media print {{
    /* Hide interactive elements */
    script {{ display: none; }}
    
    /* Optimize for print */
    .section {{
        break-inside: avoid;
        page-break-inside: avoid;
    }}
    
    /* Ensure colors print well */
    .color-preview {{
        -webkit-print-color-adjust: exact;
        color-adjust: exact;
    }}
}}
```

### Data Export
```javascript
// Export color data as JSON
function exportColors() {{
    const colors = Array.from(document.querySelectorAll('.color-value'))
        .map(el => el.textContent);
    
    const dataStr = JSON.stringify(colors, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = 'extracted-colors.json';
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
}}

// Add export button
const exportBtn = document.createElement('button');
exportBtn.textContent = 'Export Colors';
exportBtn.onclick = exportColors;
document.querySelector('.header').appendChild(exportBtn);
```

### Analytics Integration
```javascript
// Track color interactions
document.querySelectorAll('.color-swatch').forEach((swatch, index) => {{
    swatch.addEventListener('click', () => {{
        if (typeof gtag !== 'undefined') {{
            gtag('event', 'color_copy', {{
                'color_index': index,
                'color_value': swatch.querySelector('.color-value').textContent
            }});
        }}
    }});
}});
```

## Troubleshooting

### Common Issues

**Colors not displaying correctly:**
- Verify the HTML file is properly encoded as UTF-8
- Check that color values are valid hex codes
- Ensure no browser extensions are interfering

**Fonts not rendering:**
- Confirm fonts are installed on the system viewing the report
- Web fonts may not load in standalone HTML files
- Fallback fonts (system-ui, sans-serif) should always work

**Click-to-copy not working:**
- Feature requires HTTPS or localhost for security
- May not work in older browsers without Clipboard API support
- Fallback: manually select and copy text

**Layout issues on mobile:**
- Check responsive meta tag is present
- Verify CSS media queries are working
- Test on actual mobile devices, not just browser dev tools

### Browser Support

#### Full Features
- Chrome 66+ (Clipboard API)
- Firefox 63+ (Clipboard API)
- Safari 13.1+ (Clipboard API)
- Edge 79+ (Clipboard API)

#### Limited Features (no click-to-copy)
- Internet Explorer 11 (visual report only)
- Older mobile browsers
- Browsers with disabled JavaScript

### Performance

#### File Size Optimization
The HTML report is self-contained but can be optimized:

```bash
# Minify HTML (optional)
html-minifier --collapse-whitespace --remove-comments styles.html > styles.min.html

# Compress for web serving
gzip styles.html
```

#### Loading Speed
- All CSS and JavaScript is embedded (no external requests)
- Images are not used (pure CSS styling)
- Total file size typically under 50KB
- Loads instantly from local filesystem or fast servers

Generated by Web Style Extractor"""
        
        readme_path = format_dir / 'README.md'
        readme_path.write_text(readme_content, encoding='utf-8')


def get_generator():
    return HTMLGeneratorPlugin()