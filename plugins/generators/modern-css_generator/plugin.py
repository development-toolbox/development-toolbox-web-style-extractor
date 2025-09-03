"""
Modern CSS Generator Plugin
Generates cutting-edge CSS with OKLCH colors, container queries, and modern features
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any
from plugins.base_plugin import BaseGenerator


class ModernCSSGeneratorPlugin(BaseGenerator):
    """Generates modern CSS with cutting-edge features"""
    
    @property
    def name(self) -> str:
        return "Modern CSS Generator"
    
    @property
    def output_format(self) -> str:
        return "modern-css"
    
    @property
    def description(self) -> str:
        return "Cutting-edge CSS with OKLCH colors, container queries, fluid typography, and design tokens"
    
    @property
    def emoji(self) -> str:
        return "🚀"
        
    @property
    def short_description(self) -> str:
        return "Cutting-edge CSS with OKLCH and container queries"
        
    @property
    def file_extension(self) -> str:
        return "css"
    
    @property
    def capabilities(self) -> list:
        return [
            'OKLCH color space',
            'Container queries', 
            'Fluid typography with clamp()',
            'CSS custom properties',
            'Relative color syntax',
            'Modern selectors (:has, :is, :where)'
        ]
    
    @property
    def use_cases(self) -> list:
        return [
            'Modern web applications',
            'Progressive enhancement',
            'Future-proof styling',
            'Component libraries'
        ]
    
    def generate(self, extraction_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
        """Generate Modern CSS output"""
        try:
            # Get extraction data
            color_data = extraction_data.get('color_extractor', {})
            font_data = extraction_data.get('font_extractor', {})
            html_data = extraction_data.get('html_extractor', {})
            
            # Build CSS content
            content = self._generate_modern_css_content(color_data, font_data, html_data)
            
            # Write output file
            if output_path:
                # Create format-specific directory
                format_dir = Path(output_path) / 'modern-css'
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
                
                logging.info(f"✅ Modern CSS generated: {output_file}")
                
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
            logging.error(f"Modern CSS generation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _generate_modern_css_content(self, color_data: dict, font_data: dict, html_data: dict) -> str:
        """Generate modern CSS with cutting-edge features"""
        
        css_lines = []
        
        # CSS header
        css_lines.append("/* Modern CSS with cutting-edge features */")
        css_lines.append("/* Generated with Web Style Extractor */")
        css_lines.append("")
        
        # Modern CSS reset
        css_lines.append("/* Modern CSS reset */")
        css_lines.append("*, *::before, *::after {")
        css_lines.append("  box-sizing: border-box;")
        css_lines.append("}")
        css_lines.append("")
        css_lines.append("html {")
        css_lines.append("  font-size: clamp(1rem, 2.5vw, 1.125rem);")
        css_lines.append("}")
        css_lines.append("")
        
        # CSS Custom Properties (Design Tokens)
        css_lines.append(":root {")
        css_lines.append("  /* Color system with OKLCH */")
        
        colors = color_data.get('colors', [])
        for i, color in enumerate(colors[:8]):  # Limit to 8 colors
            var_name = f"--color-{i+1}"
            # Convert to OKLCH (simplified - would need proper color conversion)
            oklch_color = self._to_oklch_approximation(color)
            css_lines.append(f"  {var_name}: {color};")
            css_lines.append(f"  {var_name}-oklch: {oklch_color};")
            
            # Create variations using relative color syntax
            css_lines.append(f"  {var_name}-light: oklch(from {oklch_color} calc(l + 0.2) c h);")
            css_lines.append(f"  {var_name}-dark: oklch(from {oklch_color} calc(l - 0.2) c h);")
        
        css_lines.append("")
        css_lines.append("  /* Typography system */")
        
        fonts = font_data.get('fonts', [])
        if fonts:
            css_lines.append(f"  --font-primary: {fonts[0]}, system-ui, sans-serif;")
            if len(fonts) > 1:
                css_lines.append(f"  --font-secondary: {fonts[1]}, system-ui, sans-serif;")
            if len(fonts) > 2:
                css_lines.append(f"  --font-display: {fonts[2]}, system-ui, sans-serif;")
        
        # Fluid typography
        css_lines.append("  --text-xs: clamp(0.75rem, 2vw, 0.875rem);")
        css_lines.append("  --text-sm: clamp(0.875rem, 2.5vw, 1rem);")
        css_lines.append("  --text-base: clamp(1rem, 2.5vw, 1.125rem);")
        css_lines.append("  --text-lg: clamp(1.125rem, 3vw, 1.25rem);")
        css_lines.append("  --text-xl: clamp(1.25rem, 3.5vw, 1.5rem);")
        css_lines.append("  --text-2xl: clamp(1.5rem, 4vw, 2rem);")
        
        # Spacing system
        css_lines.append("")
        css_lines.append("  /* Spacing system */")
        css_lines.append("  --space-xs: clamp(0.25rem, 1vw, 0.5rem);")
        css_lines.append("  --space-sm: clamp(0.5rem, 2vw, 1rem);")
        css_lines.append("  --space-md: clamp(1rem, 3vw, 1.5rem);")
        css_lines.append("  --space-lg: clamp(1.5rem, 4vw, 2rem);")
        css_lines.append("  --space-xl: clamp(2rem, 5vw, 3rem);")
        
        css_lines.append("}")
        css_lines.append("")
        
        # Modern selectors and features
        css_lines.append("/* Modern CSS features */")
        css_lines.append("body {")
        body_bg = html_data.get('body_background', '#ffffff')
        css_lines.append(f"  background: {body_bg};")
        css_lines.append("  font-family: var(--font-primary);")
        css_lines.append("  font-size: var(--text-base);")
        css_lines.append("  line-height: 1.6;")
        css_lines.append("}")
        css_lines.append("")
        
        # Container queries
        css_lines.append("/* Container queries */")
        css_lines.append(".card {")
        css_lines.append("  container-type: inline-size;")
        css_lines.append("  container-name: card;")
        css_lines.append("}")
        css_lines.append("")
        css_lines.append("@container card (min-width: 400px) {")
        css_lines.append("  .card-content {")
        css_lines.append("    display: grid;")
        css_lines.append("    grid-template-columns: 1fr 2fr;")
        css_lines.append("    gap: var(--space-md);")
        css_lines.append("  }")
        css_lines.append("}")
        css_lines.append("")
        
        # Modern selectors
        css_lines.append("/* Modern selectors */")
        css_lines.append(".component:where(.primary, .secondary) {")
        css_lines.append("  padding: var(--space-md);")
        css_lines.append("  border-radius: 0.5rem;")
        css_lines.append("}")
        css_lines.append("")
        css_lines.append(".layout:has(.sidebar) .main-content {")
        css_lines.append("  margin-inline-start: 250px;")
        css_lines.append("}")
        css_lines.append("")
        
        # Utility classes
        css_lines.append("/* Utility classes */")
        for i in range(min(4, len(colors))):
            css_lines.append(f".bg-color-{i+1} {{ background: var(--color-{i+1}-oklch); }}")
            css_lines.append(f".text-color-{i+1} {{ color: var(--color-{i+1}-oklch); }}")
        
        css_lines.append("")
        css_lines.append(".text-fluid { font-size: var(--text-base); }")
        css_lines.append(".text-responsive { font-size: clamp(1rem, 4vw, 2rem); }")
        
        return "\\n".join(css_lines)
    
    def _to_oklch_approximation(self, color: str) -> str:
        """Simple approximation to OKLCH - would need proper color conversion in production"""
        # This is a simplified approximation - in production, use a proper color library
        if color.startswith('#'):
            # Rough approximation for demo purposes
            return f"oklch(65% 0.15 180deg)"
        return f"oklch(65% 0.15 180deg)"
    
    def _create_format_readme(self, format_dir: Path, color_data: dict, font_data: dict):
        """Create format-specific README with usage instructions"""
        readme_content = f"""# Modern CSS Format Usage

This directory contains the extracted styles using cutting-edge CSS features.

## Files
- `styles.css` - Modern CSS with OKLCH colors, container queries, and fluid typography

## Modern CSS Features

### OKLCH Color Space
Uses the modern OKLCH color space for better color perception and manipulation:

```css
:root {{
  --color-1-oklch: oklch(65% 0.15 180deg);
  --color-1-light: oklch(from var(--color-1-oklch) calc(l + 0.2) c h);
  --color-1-dark: oklch(from var(--color-1-oklch) calc(l - 0.2) c h);
}}

/* Usage */
.element {{
  background: var(--color-1-oklch);
  color: var(--color-1-light);
}}
```

### Container Queries
Responsive components based on container size, not viewport:

```css
.card {{
  container-type: inline-size;
  container-name: card;
}}

@container card (min-width: 400px) {{
  .card-content {{
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: var(--space-md);
  }}
}}
```

### Fluid Typography
Scaling typography that responds smoothly to screen size:

```css
:root {{
  --text-base: clamp(1rem, 2.5vw, 1.125rem);
  --text-xl: clamp(1.25rem, 3.5vw, 1.5rem);
}}

.heading {{
  font-size: var(--text-xl);
}}
```

## Browser Support

### Required Features
- **OKLCH Colors:** Chrome 111+, Firefox 113+, Safari 15.4+
- **Container Queries:** Chrome 105+, Firefox 110+, Safari 16+
- **Relative Color Syntax:** Chrome 119+, Firefox 120+, Safari 16.4+
- **Modern Selectors (:has, :is, :where):** Chrome 88+, Firefox 78+, Safari 14+

### Progressive Enhancement
```css
/* Fallback for older browsers */
.element {{
  background: #ff0000; /* Fallback */
  background: var(--color-1-oklch); /* Modern */
}}

/* Feature detection */
@supports (color: oklch(65% 0.15 180deg)) {{
  .element {{
    background: var(--color-1-oklch);
  }}
}}
```

## Usage Examples

### Basic Setup
```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="modern-css/styles.css">
</head>
<body>
    <!-- Your modern CSS content -->
</body>
</html>
```

### Component with Container Queries
```html
<div class="card">
    <div class="card-content">
        <div class="card-image">Image</div>
        <div class="card-text">Text content that reflows based on container size</div>
    </div>
</div>
```

### Fluid Typography
```html
<h1 class="text-responsive">This heading scales smoothly</h1>
<p class="text-fluid">This paragraph uses fluid font sizing</p>
```

### Modern Selectors
```html
<div class="layout">
    <aside class="sidebar">Sidebar</aside>
    <main class="main-content">Main content automatically adjusts when sidebar is present</main>
</div>

<div class="component primary">Uses :where() selector</div>
<div class="component secondary">Also uses :where() selector</div>
```

## Framework Integration

### React with Modern CSS
```jsx
function ModernComponent() {{
  return (
    <div className="card">
      <div className="card-content">
        <h2 style={{{{ fontSize: 'var(--text-xl)' }}}}>Modern Heading</h2>
        <p className="bg-color-1 text-color-2">Using OKLCH colors</p>
      </div>
    </div>
  );
}}
```

### Vue with Container Queries
```vue
<template>
  <div class="card">
    <div class="card-content">
      <h2>Vue Component</h2>
      <p>Responsive layout using container queries</p>
    </div>
  </div>
</template>

<style scoped>
/* Component-specific modern CSS */
.card {{
  container-type: inline-size;
}}

@container (min-width: 300px) {{
  .card-content {{
    padding: var(--space-lg);
  }}
}}
</style>
```

### Next.js Integration
```javascript
// next.config.js
module.exports = {{
  experimental: {{
    // Enable modern CSS features
    cssChunking: true,
  }},
  webpack: (config) => {{
    // Modern CSS processing
    return config;
  }}
}}
```

## Build Tools

### PostCSS Configuration
```javascript
// postcss.config.js
module.exports = {{
  plugins: [
    require('postcss-preset-env')({
      stage: 1, // Enable cutting-edge features
      features: {{
        'oklab-function': true,
        'relative-color-syntax': true,
        'container-queries': true
      }}
    }},
    require('autoprefixer')
  ]
}}
```

### Vite Configuration
```javascript
// vite.config.js
export default {{
  css: {{
    postcss: {{
      plugins: [
        require('postcss-preset-env')({
          stage: 1,
          features: {{
            'custom-properties': false, // Don't transpile CSS custom properties
            'oklab-function': true,
            'container-queries': true
          }}
        })
      ]
    }}
  }}
}}
```

## Color System

### OKLCH Benefits
- **Perceptually uniform:** Equal numeric changes produce equal visual changes
- **Wide gamut:** Supports P3 and Rec2020 color spaces  
- **Predictable:** Lightness, chroma, and hue are independent
- **Future-proof:** Native browser support growing rapidly

### Color Manipulation
```css
/* Create color variations */
.primary-variants {{
  background: var(--color-1-oklch);
  border-color: var(--color-1-light);
  box-shadow: 0 4px 12px var(--color-1-dark);
}}

/* Smooth color transitions */
.animated-color {{
  background: var(--color-1-oklch);
  transition: background 0.3s ease;
}}

.animated-color:hover {{
  background: var(--color-1-light);
}}
```

## Performance Considerations

### Modern CSS Benefits
- **Container queries** reduce JavaScript layout calculations
- **OKLCH colors** provide better compression than RGB/HSL
- **Fluid typography** eliminates media query breakpoints
- **Modern selectors** reduce CSS specificity conflicts

### Optimization Tips
```css
/* Use logical properties for better i18n */
.element {{
  margin-inline: var(--space-md);
  padding-block: var(--space-sm);
}}

/* Combine modern features */
@container (min-width: 400px) {{
  .responsive-text {{
    font-size: clamp(1rem, 3vw, 2rem);
    color: oklch(from var(--color-primary) calc(l * 0.9) c h);
  }}
}}
```

## Migration Guide

### From Traditional CSS
1. **Colors:** Replace hex/rgb with OKLCH variables
2. **Media queries:** Consider container queries for components  
3. **Fixed font sizes:** Switch to fluid typography
4. **Complex selectors:** Simplify with :is() and :where()

### Gradual Adoption
```css
/* Phase 1: Add fallbacks */
.element {{
  background: #ff0000;
  background: var(--color-1-oklch);
}}

/* Phase 2: Use feature detection */
@supports (container-type: inline-size) {{
  .card {{
    container-type: inline-size;
  }}
}}

/* Phase 3: Full modern CSS */
@container (min-width: 400px) {{
  .modern-layout {{
    display: grid;
    color: oklch(from var(--primary) calc(l + 0.1) c h);
  }}
}}
```

Generated by Web Style Extractor"""
        
        readme_path = format_dir / 'README.md'
        readme_path.write_text(readme_content, encoding='utf-8')


def get_generator():
    return ModernCSSGeneratorPlugin()