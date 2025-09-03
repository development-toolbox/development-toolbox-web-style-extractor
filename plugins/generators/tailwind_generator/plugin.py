"""
Tailwind CSS Generator Plugin
Generates Tailwind CSS configuration with extracted color palettes and font families
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any
from plugins.base_plugin import BaseGenerator


class TailwindGeneratorPlugin(BaseGenerator):
    """Generates Tailwind CSS configuration"""
    
    @property
    def name(self) -> str:
        return "Tailwind CSS Generator"
    
    @property
    def output_format(self) -> str:
        return "tailwind"
    
    @property
    def description(self) -> str:
        return "Complete Tailwind CSS configuration with extracted color palettes and font families"
    
    @property
    def emoji(self) -> str:
        return "⚡"
        
    @property
    def short_description(self) -> str:
        return "Tailwind configuration with custom colors and fonts"
        
    @property
    def file_extension(self) -> str:
        return "js"
    
    @property
    def capabilities(self) -> list:
        return [
            'Custom color palettes',
            'Font family configuration', 
            'Spacing scales',
            'Component classes',
            'Dark mode variants'
        ]
    
    @property
    def use_cases(self) -> list:
        return [
            'Tailwind CSS projects',
            'Rapid prototyping',
            'Component libraries',
            'Design system implementation'
        ]
    
    def generate(self, extraction_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
        """Generate Tailwind CSS configuration"""
        try:
            # Get extraction data
            color_data = extraction_data.get('color_extractor', {})
            font_data = extraction_data.get('font_extractor', {})
            html_data = extraction_data.get('html_extractor', {})
            
            # Build Tailwind config
            config = self._generate_tailwind_config(color_data, font_data, html_data)
            
            # Convert to JavaScript module format
            content = self._format_as_js_module(config)
            
            # Write output file
            if output_path:
                # Create format-specific directory
                format_dir = Path(output_path) / 'tailwind'
                format_dir.mkdir(exist_ok=True)
                
                # Build file path inside format_dir
                output_file = format_dir / f'tailwind.config.{self.file_extension}'
                
                # Check if file exists and archive using base class method
                if output_file.exists():
                    self.archive_existing_file(output_file, format_dir)
                
                # Write new file to format_dir
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Create format-specific README
                self._create_format_readme(format_dir, config)
                
                logging.info(f"✅ Tailwind configuration generated: {output_file}")
                
                return {
                    'success': True,
                    'file': str(output_file),
                    'format': self.output_format,
                    'content': content,
                    'config': config
                }
            else:
                return {
                    'success': True, 
                    'format': self.output_format,
                    'content': content,
                    'config': config
                }
                
        except Exception as e:
            logging.error(f"Tailwind configuration generation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _generate_tailwind_config(self, color_data: dict, font_data: dict, html_data: dict) -> dict:
        """Generate Tailwind CSS configuration object"""
        
        config = {
            "content": [
                "./src/**/*.{js,jsx,ts,tsx}",
                "./pages/**/*.{js,jsx,ts,tsx}",
                "./components/**/*.{js,jsx,ts,tsx}",
                "./public/**/*.html"
            ],
            "theme": {
                "extend": {
                    "colors": {},
                    "fontFamily": {},
                    "spacing": {},
                    "borderRadius": {},
                    "boxShadow": {}
                }
            },
            "plugins": []
        }
        
        # Process colors
        colors = color_data.get('colors', [])
        if colors:
            # Create semantic color names
            config["theme"]["extend"]["colors"] = {
                "primary": colors[0] if len(colors) > 0 else "#3b82f6",
                "secondary": colors[1] if len(colors) > 1 else "#64748b",
                "accent": colors[2] if len(colors) > 2 else "#06d6a0",
                "background": html_data.get('body_background', '#ffffff'),
            }
            
            # Add extracted color palette
            extracted_colors = {}
            for i, color in enumerate(colors[:10]):  # Limit to 10 colors
                color_name = f"extracted-{i+1}"
                extracted_colors[color_name] = color
            
            config["theme"]["extend"]["colors"]["extracted"] = extracted_colors
        
        # Process fonts
        fonts = font_data.get('fonts', [])
        if fonts:
            # Clean font names and create font families
            clean_fonts = []
            for font in fonts[:5]:  # Limit to 5 fonts
                # Remove quotes and clean font names
                clean_font = font.replace('"', '').replace("'", "")
                if clean_font not in ['serif', 'sans-serif', 'monospace', 'inherit', 'initial', 'unset']:
                    clean_fonts.append(clean_font)
            
            if clean_fonts:
                config["theme"]["extend"]["fontFamily"] = {
                    "primary": [clean_fonts[0], "system-ui", "sans-serif"],
                    "secondary": [clean_fonts[1], "system-ui", "sans-serif"] if len(clean_fonts) > 1 else ["system-ui", "sans-serif"],
                    "display": [clean_fonts[2], "system-ui", "sans-serif"] if len(clean_fonts) > 2 else ["system-ui", "sans-serif"]
                }
        
        # Add custom spacing scale
        config["theme"]["extend"]["spacing"] = {
            "18": "4.5rem",
            "88": "22rem",
            "112": "28rem",
            "128": "32rem"
        }
        
        # Add custom border radius
        config["theme"]["extend"]["borderRadius"] = {
            "4xl": "2rem",
            "5xl": "2.5rem"
        }
        
        # Add custom box shadows
        config["theme"]["extend"]["boxShadow"] = {
            "soft": "0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)",
            "brand": f"0 4px 14px 0 {colors[0] if colors else '#3b82f6'}40"
        }
        
        return config
    
    def _format_as_js_module(self, config: dict) -> str:
        """Format config as JavaScript module"""
        
        # Convert Python dict to JavaScript object string
        js_config = json.dumps(config, indent=2)
        
        # Replace JSON quotes with JavaScript syntax where appropriate
        js_config = js_config.replace('"content":', 'content:')
        js_config = js_config.replace('"theme":', 'theme:')
        js_config = js_config.replace('"extend":', 'extend:')
        js_config = js_config.replace('"plugins":', 'plugins:')
        
        content = f'''/** @type {{import('tailwindcss').Config}} */
module.exports = {js_config}

/*
Usage Examples:

1. In your HTML/JSX:
   <div className="bg-primary text-white font-primary">
     Primary styled content
   </div>
   
   <div className="bg-extracted-1 text-secondary font-secondary">
     Using extracted colors and fonts
   </div>

2. Custom utility classes:
   <div className="shadow-soft rounded-4xl p-18">
     Custom spacing and shadows
   </div>
   
3. Responsive design:
   <div className="bg-primary md:bg-secondary lg:bg-accent">
     Responsive background colors
   </div>

4. Dark mode (if enabled):
   <div className="bg-primary dark:bg-secondary">
     Dark mode support
   </div>
*/'''
        
        return content
    
    def _create_format_readme(self, format_dir: Path, config: dict):
        """Create format-specific README with usage instructions"""
        readme_content = f"""# Tailwind CSS Configuration Usage

This directory contains the extracted styles in Tailwind CSS format.

## Files
- `tailwind.config.js` - Complete Tailwind CSS configuration with custom colors and fonts

## Installation & Setup

### 1. Install Tailwind CSS
```bash
npm install -D tailwindcss
# or
yarn add -D tailwindcss
```

### 2. Use This Configuration
Replace your existing `tailwind.config.js` with the generated file, or merge the configurations:

```javascript
// tailwind.config.js
const extractedConfig = require('./tailwind/tailwind.config.js');

module.exports = {{
  ...extractedConfig,
  // Add your own customizations here
  content: [
    ...extractedConfig.content,
    // Add your own content paths
  ]
}}
```

## Usage Examples

### Custom Colors
```html
<!-- Primary colors from extracted palette -->
<div class="bg-primary text-white">Primary Background</div>
<div class="bg-secondary text-white">Secondary Background</div>
<div class="bg-accent text-white">Accent Color</div>

<!-- Specific extracted colors -->
<div class="bg-extracted-1">First extracted color</div>
<div class="bg-extracted-2">Second extracted color</div>
```

### Custom Fonts
```html
<!-- Using extracted font families -->
<h1 class="font-primary">Primary Font Heading</h1>
<h2 class="font-secondary">Secondary Font Heading</h2>
<p class="font-display">Display Font Text</p>
```

### Custom Spacing & Effects
```html
<!-- Custom spacing values -->
<div class="p-18 m-88">Custom padding and margin</div>

<!-- Custom border radius -->
<div class="rounded-4xl">Large rounded corners</div>

<!-- Custom shadows -->
<div class="shadow-soft">Soft shadow effect</div>
<div class="shadow-brand">Brand-colored shadow</div>
```

### React/JSX Example
```jsx
function MyComponent() {{
  return (
    <div className="bg-primary text-white font-primary p-18 rounded-4xl shadow-soft">
      <h2 className="font-display text-2xl mb-4">Styled with Extracted Theme</h2>
      <p className="font-secondary">This component uses the extracted colors and fonts.</p>
      <button className="bg-accent hover:bg-extracted-1 px-6 py-3 rounded-lg transition-colors">
        Custom Button
      </button>
    </div>
  );
}}
```

### Vue Example
```vue
<template>
  <div class="bg-secondary text-white font-primary p-18">
    <h1 class="font-display text-3xl">Vue Component</h1>
    <p class="font-secondary">Using extracted Tailwind theme</p>
  </div>
</template>
```

## Integration with Frameworks

### Next.js
```javascript
// next.config.js
module.exports = {{
  content: [
    './pages/**/*.{{js,ts,jsx,tsx}}',
    './components/**/*.{{js,ts,jsx,tsx}}',
  ],
  // ... rest of your Tailwind config
}}
```

### Vite
```javascript
// vite.config.js
export default {{
  css: {{
    postcss: {{
      plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
      ],
    }},
  }},
}}
```

### Build Process
```bash
# Build your CSS
npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch

# Or with PostCSS
npm run build:css
```

## Customization

The generated configuration is fully customizable. You can:

- Add more colors to the palette
- Modify font stacks
- Adjust spacing scale
- Add custom plugins
- Configure dark mode variants

```javascript
// Extend the generated config
module.exports = {{
  ...require('./tailwind.config.js'),
  theme: {{
    extend: {{
      // Your additional customizations
      animation: {{
        'bounce-slow': 'bounce 2s infinite',
      }}
    }}
  }},
  plugins: [
    // Add custom plugins
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ]
}}
```

Generated by Web Style Extractor"""
        
        readme_path = format_dir / 'README.md'
        readme_path.write_text(readme_content, encoding='utf-8')


def get_generator():
    return TailwindGeneratorPlugin()