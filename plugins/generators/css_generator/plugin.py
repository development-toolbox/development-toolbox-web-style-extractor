"""
CSS variables generator - generates CSS custom properties and utility classes
"""
import os
from datetime import datetime
from pathlib import Path
from plugins.base_plugin import BaseGenerator
from typing import Dict, Any


class CSSGenerator(BaseGenerator):
    @property
    def name(self):
        return "css_generator"
    
    @property
    def output_format(self):
        return "css"
    
    def generate(self, extraction_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
        """Generate CSS variables from extraction data"""
        
        css_content = self._generate_css_content(extraction_data)
        
        if output_path:
            # Create format-specific directory
            format_dir = Path(output_path) / 'css'
            format_dir.mkdir(exist_ok=True)
            
            # Build file path inside format_dir
            css_path = format_dir / 'styles.css'
            
            # Check if file exists and archive using base class method
            if css_path.exists():
                self.archive_existing_file(css_path, format_dir)
            
            # Write new file to format_dir
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
            
            # Create format-specific README
            self._create_format_readme(format_dir, extraction_data)
            
            return {'file': str(css_path), 'content': css_content}
        
        return {'content': css_content}
    
    def _generate_css_content(self, data: Dict[str, Any]) -> str:
        """Generate complete CSS content"""
        css_parts = []
        
        # Header comment
        css_parts.append(self._generate_header_comment(data))
        
        # CSS Custom Properties (Variables)
        css_parts.append(self._generate_css_variables(data))
        
        # Utility Classes
        css_parts.append(self._generate_utility_classes(data))
        
        # Typography Classes
        css_parts.append(self._generate_typography_classes(data))
        
        # Component Classes
        css_parts.append(self._generate_component_classes(data))
        
        return '\n\n'.join(filter(None, css_parts))
    
    def _generate_header_comment(self, data: Dict[str, Any]) -> str:
        """Generate header comment with extraction info"""
        url = data.get('url', 'Unknown')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return f"""/*
 * CSS Design System
 * Generated from: {url}
 * Generated at: {timestamp}
 * Generator: Web Style Extractor v2.0
 *
 * This file contains CSS custom properties and utility classes
 * extracted and generated from the source website's design system.
 */"""
    
    def _generate_css_variables(self, data: Dict[str, Any]) -> str:
        """Generate CSS custom properties"""
        css_lines = [":root {"]
        
        # Color variables
        if 'color_extractor' in data.get('extraction', {}):
            color_data = data['extraction']['color_extractor']
            css_lines.append("  /* Colors */")
            
            colors = color_data.get('colors', [])
            for i, color in enumerate(colors[:12]):
                css_lines.append(f"  --color-{i+1}: {color};")
            
            # Semantic color variables
            palette = color_data.get('color_palette', {})
            if palette.get('primary'):
                css_lines.append(f"  --color-primary: {palette['primary']};")
            if palette.get('secondary'):
                css_lines.append(f"  --color-secondary: {palette['secondary']};")
            if palette.get('accent'):
                css_lines.append(f"  --color-accent: {palette['accent']};")
            if palette.get('background'):
                css_lines.append(f"  --color-background: {palette['background']};")
            if palette.get('text'):
                css_lines.append(f"  --color-text: {palette['text']};")
            
            # Color variations
            variations = palette.get('variations', {})
            if variations.get('light'):
                css_lines.append(f"  --color-primary-light: {variations['light']};")
            if variations.get('dark'):
                css_lines.append(f"  --color-primary-dark: {variations['dark']};")
        
        # Font variables
        if 'font_extractor' in data.get('extraction', {}):
            font_data = data['extraction']['font_extractor']
            css_lines.append("")
            css_lines.append("  /* Typography */")
            
            fonts = font_data.get('fonts', [])
            for i, font in enumerate(fonts[:6]):
                # Create font stacks with fallbacks
                if any(serif in font.lower() for serif in ['times', 'georgia', 'serif']):
                    fallback = ', serif'
                elif any(mono in font.lower() for mono in ['courier', 'monaco', 'mono']):
                    fallback = ', monospace'
                else:
                    fallback = ', system-ui, sans-serif'
                
                css_lines.append(f"  --font-{i+1}: '{font}'{fallback};")
            
            # Semantic font variables
            if fonts:
                css_lines.append(f"  --font-primary: '{fonts[0]}', system-ui, sans-serif;")
                if len(fonts) > 1:
                    css_lines.append(f"  --font-secondary: '{fonts[1]}', system-ui, sans-serif;")
                if len(fonts) > 2:
                    css_lines.append(f"  --font-accent: '{fonts[2]}', system-ui, sans-serif;")
        
        # Spacing variables
        css_lines.append("")
        css_lines.append("  /* Spacing */")
        css_lines.extend([
            "  --space-xs: 0.25rem;",
            "  --space-sm: 0.5rem;",
            "  --space-md: 1rem;",
            "  --space-lg: 1.5rem;",
            "  --space-xl: 2rem;",
            "  --space-2xl: 3rem;"
        ])
        
        # Border radius
        css_lines.append("")
        css_lines.append("  /* Border Radius */")
        css_lines.extend([
            "  --radius-sm: 0.25rem;",
            "  --radius-md: 0.5rem;",
            "  --radius-lg: 1rem;",
            "  --radius-full: 9999px;"
        ])
        
        # Shadows
        css_lines.append("")
        css_lines.append("  /* Shadows */")
        css_lines.extend([
            "  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.1);",
            "  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);",
            "  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);",
            "  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);"
        ])
        
        css_lines.append("}")
        return '\n'.join(css_lines)
    
    def _generate_utility_classes(self, data: Dict[str, Any]) -> str:
        """Generate utility classes for colors"""
        css_lines = ["/* Utility Classes */"]
        
        if 'color_extractor' in data.get('extraction', {}):
            color_data = data['extraction']['color_extractor']
            colors = color_data.get('colors', [])
            
            # Color utilities
            for i, color in enumerate(colors[:8]):
                class_name = f"color-{i+1}"
                css_lines.extend([
                    f".text-{class_name} {{ color: var(--color-{i+1}); }}",
                    f".bg-{class_name} {{ background-color: var(--color-{i+1}); }}",
                    f".border-{class_name} {{ border-color: var(--color-{i+1}); }}"
                ])
            
            # Semantic color utilities
            palette = color_data.get('color_palette', {})
            for semantic_name in ['primary', 'secondary', 'accent']:
                if palette.get(semantic_name):
                    css_lines.extend([
                        f".text-{semantic_name} {{ color: var(--color-{semantic_name}); }}",
                        f".bg-{semantic_name} {{ background-color: var(--color-{semantic_name}); }}",
                        f".border-{semantic_name} {{ border-color: var(--color-{semantic_name}); }}"
                    ])
        
        return '\n'.join(css_lines)
    
    def _generate_typography_classes(self, data: Dict[str, Any]) -> str:
        """Generate typography classes"""
        css_lines = ["/* Typography Classes */"]
        
        # Font family classes
        if 'font_extractor' in data.get('extraction', {}):
            font_data = data['extraction']['font_extractor']
            fonts = font_data.get('fonts', [])
            
            for i, font in enumerate(fonts[:4]):
                css_lines.append(f".font-{i+1} {{ font-family: var(--font-{i+1}); }}")
            
            # Semantic font classes
            if fonts:
                css_lines.extend([
                    ".font-primary { font-family: var(--font-primary); }",
                    ".font-secondary { font-family: var(--font-secondary); }" if len(fonts) > 1 else "",
                    ".font-accent { font-family: var(--font-accent); }" if len(fonts) > 2 else ""
                ])
        
        # Typography scale classes
        css_lines.extend([
            "",
            "/* Typography Scale */",
            ".text-xs { font-size: 0.75rem; line-height: 1rem; }",
            ".text-sm { font-size: 0.875rem; line-height: 1.25rem; }",
            ".text-base { font-size: 1rem; line-height: 1.5rem; }",
            ".text-lg { font-size: 1.125rem; line-height: 1.75rem; }",
            ".text-xl { font-size: 1.25rem; line-height: 1.75rem; }",
            ".text-2xl { font-size: 1.5rem; line-height: 2rem; }",
            ".text-3xl { font-size: 1.875rem; line-height: 2.25rem; }",
            ".text-4xl { font-size: 2.25rem; line-height: 2.5rem; }"
        ])
        
        return '\n'.join(filter(None, css_lines))
    
    def _generate_component_classes(self, data: Dict[str, Any]) -> str:
        """Generate common component classes"""
        css_lines = ["/* Component Classes */"]
        
        # Button component
        css_lines.extend([
            ".btn {",
            "  display: inline-flex;",
            "  align-items: center;",
            "  justify-content: center;",
            "  padding: var(--space-sm) var(--space-md);",
            "  border: 1px solid transparent;",
            "  border-radius: var(--radius-md);",
            "  font-family: var(--font-primary);",
            "  font-weight: 500;",
            "  text-decoration: none;",
            "  transition: all 0.2s ease;",
            "  cursor: pointer;",
            "}",
            "",
            ".btn-primary {",
            "  background-color: var(--color-primary);",
            "  color: white;",
            "}",
            "",
            ".btn-secondary {",
            "  background-color: transparent;",
            "  color: var(--color-primary);",
            "  border-color: var(--color-primary);",
            "}",
            "",
            ".btn:hover {",
            "  transform: translateY(-1px);",
            "  box-shadow: var(--shadow-md);",
            "}"
        ])
        
        # Card component
        css_lines.extend([
            "",
            ".card {",
            "  background: var(--color-background, white);",
            "  border-radius: var(--radius-lg);",
            "  padding: var(--space-lg);",
            "  box-shadow: var(--shadow-sm);",
            "  border: 1px solid rgba(0, 0, 0, 0.1);",
            "}",
            "",
            ".card-header {",
            "  font-family: var(--font-primary);",
            "  font-size: 1.25rem;",
            "  font-weight: 600;",
            "  color: var(--color-text);",
            "  margin-bottom: var(--space-md);",
            "}"
        ])
        
        # Container classes
        css_lines.extend([
            "",
            ".container {",
            "  width: 100%;",
            "  max-width: 1200px;",
            "  margin: 0 auto;",
            "  padding: 0 var(--space-md);",
            "}",
            "",
            ".flex { display: flex; }",
            ".flex-col { flex-direction: column; }",
            ".items-center { align-items: center; }",
            ".justify-center { justify-content: center; }",
            ".gap-sm { gap: var(--space-sm); }",
            ".gap-md { gap: var(--space-md); }",
            ".gap-lg { gap: var(--space-lg); }"
        ])
        
        return '\n'.join(css_lines)
    
    def _create_format_readme(self, format_dir: Path, extraction_data: dict):
        """Create format-specific README with usage instructions"""
        readme_content = f"""# CSS Variables Format Usage

This directory contains the extracted styles as CSS custom properties and utility classes.

## Files
- `styles.css` - Complete CSS file with custom properties, utilities, and component classes

## Quick Start

### 1. Include in Your HTML
```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <!-- Your content -->
</body>
</html>
```

### 2. Import in CSS
```css
/* In your main CSS file */
@import url('css/styles.css');

/* Or import specific parts */
@import url('css/styles.css') layer(base);
```

## CSS Custom Properties (Variables)

The generated CSS includes organized custom properties:

### Colors
```css
:root {{
  --color-primary: #ff0000;
  --color-secondary: #00ff00;
  --color-accent: #0000ff;
  --color-background: #ffffff;
  --color-text: #333333;
}}

/* Usage */
.my-element {{
  background-color: var(--color-primary);
  color: var(--color-text);
}}
```

### Typography
```css
:root {{
  --font-primary: 'Arial', system-ui, sans-serif;
  --font-secondary: 'Georgia', serif;
}}

/* Usage */
.heading {{
  font-family: var(--font-primary);
}}
```

### Spacing
```css
:root {{
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
}}

/* Usage */
.card {{
  padding: var(--space-lg);
  margin-bottom: var(--space-md);
}}
```

## Utility Classes

Ready-to-use utility classes for rapid development:

### Color Utilities
```html
<!-- Text colors -->
<p class="text-primary">Primary text color</p>
<p class="text-secondary">Secondary text color</p>

<!-- Background colors -->
<div class="bg-primary">Primary background</div>
<div class="bg-accent">Accent background</div>

<!-- Border colors -->
<div class="border-primary">Primary border</div>
```

### Typography Utilities
```html
<!-- Font families -->
<h1 class="font-primary">Primary font heading</h1>
<p class="font-secondary">Secondary font text</p>

<!-- Font sizes -->
<p class="text-sm">Small text</p>
<p class="text-base">Base text</p>
<h2 class="text-xl">Large heading</h2>
<h1 class="text-3xl">Extra large heading</h1>
```

### Layout Utilities
```html
<!-- Flexbox -->
<div class="flex items-center justify-center gap-md">
  <span>Flexbox layout</span>
</div>

<!-- Container -->
<div class="container">
  <p>Centered container with max-width</p>
</div>
```

## Component Classes

Pre-built component styles:

### Buttons
```html
<!-- Primary button -->
<button class="btn btn-primary">Primary Button</button>

<!-- Secondary button -->
<button class="btn btn-secondary">Secondary Button</button>

<!-- Custom button -->
<a href="#" class="btn" style="background: var(--color-accent);">Custom Button</a>
```

### Cards
```html
<div class="card">
  <div class="card-header">Card Title</div>
  <p>Card content goes here.</p>
</div>
```

## Framework Integration

### React/JSX
```jsx
function MyComponent() {{
  return (
    <div className="card">
      <h2 className="card-header font-primary">Component Title</h2>
      <p className="text-secondary">Using extracted CSS variables</p>
      <button className="btn btn-primary">Action Button</button>
    </div>
  );
}}
```

### Vue
```vue
<template>
  <div class="card">
    <h2 class="card-header font-primary">Vue Component</h2>
    <p class="text-secondary">Styled with extracted variables</p>
  </div>
</template>

<style scoped>
.custom-element {{
  background: var(--color-primary);
  color: var(--color-background);
}}
</style>
```

### Angular
```typescript
// component.ts
@Component({{
  selector: 'app-my-component',
  template: `
    <div class="card">
      <h2 class="card-header font-primary">Angular Component</h2>
      <p class="text-secondary">Using CSS variables</p>
    </div>
  `,
  styleUrls: ['./component.css']
}})
export class MyComponent {{}}
```

## Customization

### Override Variables
```css
/* Override default values */
:root {{
  --color-primary: #your-color;
  --font-primary: 'Your Font', sans-serif;
  --space-lg: 2rem;
}}
```

### Dark Mode Support
```css
/* Add dark mode variants */
@media (prefers-color-scheme: dark) {{
  :root {{
    --color-background: #1a1a1a;
    --color-text: #ffffff;
    --color-primary: #4a90e2;
  }}
}}

/* Or use data attribute */
[data-theme="dark"] {{
  --color-background: #1a1a1a;
  --color-text: #ffffff;
}}
```

### Responsive Design
```css
/* Responsive spacing */
@media (min-width: 768px) {{
  :root {{
    --space-md: 1.5rem;
    --space-lg: 2.5rem;
  }}
}}
```

## Build Tools Integration

### PostCSS
```javascript
// postcss.config.js
module.exports = {{
  plugins: [
    require('postcss-custom-properties')(),
    require('autoprefixer')
  ]
}}
```

### Sass/SCSS
```scss
// Import CSS variables
@import 'css/styles.css';

// Use in Sass
.my-class {{
  background: var(--color-primary);
  padding: var(--space-md);
  
  &:hover {{
    background: var(--color-secondary);
  }}
}}
```

### CSS-in-JS
```javascript
// styled-components or emotion
const StyledButton = styled.button`
  background-color: var(--color-primary);
  color: var(--color-background);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  font-family: var(--font-primary);
`;
```

Generated by Web Style Extractor"""
        
        readme_path = format_dir / 'README.md'
        readme_path.write_text(readme_content, encoding='utf-8')


def get_generator():
    return CSSGenerator()