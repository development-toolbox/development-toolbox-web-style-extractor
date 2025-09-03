"""
Design Tokens Generator Plugin
Generates Style Dictionary compatible design tokens for multi-platform use
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any
from plugins.base_plugin import BaseGenerator


class DesignTokensGeneratorPlugin(BaseGenerator):
    """Generates design tokens in Style Dictionary format"""
    
    @property
    def name(self) -> str:
        return "Design Tokens Generator"
    
    @property
    def output_format(self) -> str:
        return "design-tokens"
    
    @property
    def description(self) -> str:
        return "Comprehensive design tokens in Style Dictionary format for multi-platform generation"
    
    @property
    def emoji(self) -> str:
        return "🎯"
        
    @property
    def short_description(self) -> str:
        return "Style Dictionary compatible design tokens"
        
    @property
    def file_extension(self) -> str:
        return "json"
    
    @property
    def capabilities(self) -> list:
        return [
            'Style Dictionary format',
            'Semantic naming',
            'Platform-agnostic',
            'Typography scales',
            'Spacing systems',
            'Component tokens'
        ]
    
    @property
    def use_cases(self) -> list:
        return [
            'Cross-platform apps',
            'Design system libraries',
            'Multi-brand theming',
            'Component documentation'
        ]
    
    def generate(self, extraction_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
        """Generate Design Tokens output"""
        try:
            # Get extraction data
            color_data = extraction_data.get('color_extractor', {})
            font_data = extraction_data.get('font_extractor', {})
            html_data = extraction_data.get('html_extractor', {})
            
            # Build design tokens structure
            tokens = self._generate_design_tokens(color_data, font_data, html_data)
            
            # Write output file
            if output_path:
                # Create format-specific directory
                format_dir = Path(output_path) / 'design-tokens'
                format_dir.mkdir(exist_ok=True)
                
                # Build file path inside format_dir
                output_file = format_dir / f'design-tokens.{self.file_extension}'
                
                # Check if file exists and archive using base class method
                if output_file.exists():
                    self.archive_existing_file(output_file, format_dir)
                
                # Write new file to format_dir
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(tokens, f, indent=2, ensure_ascii=False)
                
                # Create format-specific README
                self._create_format_readme(format_dir, tokens)
                
                logging.info(f"✅ Design tokens generated: {output_file}")
                
                return {
                    'success': True,
                    'file': str(output_file),
                    'format': self.output_format,
                    'content': tokens
                }
            else:
                return {
                    'success': True, 
                    'format': self.output_format,
                    'content': tokens
                }
                
        except Exception as e:
            logging.error(f"Design tokens generation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _generate_design_tokens(self, color_data: dict, font_data: dict, html_data: dict) -> dict:
        """Generate Style Dictionary compatible design tokens"""
        
        tokens = {
            "designSystem": {
                "colors": {
                    "semantic": {},
                    "brand": {},
                    "neutral": {}
                },
                "typography": {
                    "fontFamilies": {},
                    "fontSizes": {},
                    "fontWeights": {},
                    "lineHeights": {}
                },
                "spacing": {
                    "scale": {}
                },
                "radius": {
                    "scale": {}
                }
            }
        }
        
        # Process colors
        colors = color_data.get('colors', [])
        
        # Create semantic colors
        if colors:
            tokens["designSystem"]["colors"]["semantic"] = {
                "primary": {
                    "value": colors[0],
                    "type": "color",
                    "description": "Primary brand color"
                }
            }
            
            if len(colors) > 1:
                tokens["designSystem"]["colors"]["semantic"]["secondary"] = {
                    "value": colors[1],
                    "type": "color",
                    "description": "Secondary brand color"
                }
            
            # Create brand color scale
            for i, color in enumerate(colors[:6]):  # Limit to 6 colors
                tokens["designSystem"]["colors"]["brand"][f"color-{i+1:02d}"] = {
                    "value": color,
                    "type": "color",
                    "description": f"Brand color {i+1}"
                }
        
        # Background colors from HTML data
        body_bg = html_data.get('body_background')
        if body_bg:
            tokens["designSystem"]["colors"]["semantic"]["background"] = {
                "value": body_bg,
                "type": "color",
                "description": "Main background color"
            }
        
        # Process fonts
        fonts = font_data.get('fonts', [])
        if fonts:
            # Font families
            tokens["designSystem"]["typography"]["fontFamilies"]["primary"] = {
                "value": fonts[0],
                "type": "fontFamily",
                "description": "Primary font family"
            }
            
            if len(fonts) > 1:
                tokens["designSystem"]["typography"]["fontFamilies"]["secondary"] = {
                    "value": fonts[1],
                    "type": "fontFamily",
                    "description": "Secondary font family"
                }
                
            if len(fonts) > 2:
                tokens["designSystem"]["typography"]["fontFamilies"]["display"] = {
                    "value": fonts[2],
                    "type": "fontFamily",
                    "description": "Display/heading font family"
                }
        
        # Font sizes with fluid typography
        font_sizes = {
            "xs": {"static": "0.75rem", "fluid": "clamp(0.75rem, 2vw, 0.875rem)"},
            "sm": {"static": "0.875rem", "fluid": "clamp(0.875rem, 2.5vw, 1rem)"},
            "base": {"static": "1rem", "fluid": "clamp(1rem, 2.5vw, 1.125rem)"},
            "lg": {"static": "1.125rem", "fluid": "clamp(1.125rem, 3vw, 1.25rem)"},
            "xl": {"static": "1.25rem", "fluid": "clamp(1.25rem, 3.5vw, 1.5rem)"},
            "2xl": {"static": "1.5rem", "fluid": "clamp(1.5rem, 4vw, 2rem)"},
            "3xl": {"static": "1.875rem", "fluid": "clamp(1.875rem, 5vw, 2.5rem)"}
        }
        
        for size, values in font_sizes.items():
            tokens["designSystem"]["typography"]["fontSizes"][size] = {
                "value": values["fluid"],
                "static": values["static"],
                "type": "fontSize.fluid",
                "description": f"Font size {size}"
            }
        
        # Font weights
        font_weights = {
            "light": {"value": "300", "description": "Light font weight"},
            "regular": {"value": "400", "description": "Regular font weight"},
            "medium": {"value": "500", "description": "Medium font weight"},
            "semibold": {"value": "600", "description": "Semibold font weight"},
            "bold": {"value": "700", "description": "Bold font weight"}
        }
        
        for weight, config in font_weights.items():
            tokens["designSystem"]["typography"]["fontWeights"][weight] = {
                "value": config["value"],
                "type": "fontWeight",
                "description": config["description"]
            }
        
        # Line heights
        line_heights = {
            "tight": {"value": "1.25", "description": "Tight line height"},
            "normal": {"value": "1.5", "description": "Normal line height"},
            "relaxed": {"value": "1.75", "description": "Relaxed line height"}
        }
        
        for height, config in line_heights.items():
            tokens["designSystem"]["typography"]["lineHeights"][height] = {
                "value": config["value"],
                "type": "lineHeight",
                "description": config["description"]
            }
        
        # Spacing scale
        spacing_scale = {
            "xs": {"value": "0.25rem", "fluid": "clamp(0.25rem, 1vw, 0.5rem)"},
            "sm": {"value": "0.5rem", "fluid": "clamp(0.5rem, 2vw, 1rem)"},
            "md": {"value": "1rem", "fluid": "clamp(1rem, 3vw, 1.5rem)"},
            "lg": {"value": "1.5rem", "fluid": "clamp(1.5rem, 4vw, 2rem)"},
            "xl": {"value": "2rem", "fluid": "clamp(2rem, 5vw, 3rem)"},
            "2xl": {"value": "3rem", "fluid": "clamp(3rem, 6vw, 4rem)"}
        }
        
        for size, values in spacing_scale.items():
            tokens["designSystem"]["spacing"]["scale"][size] = {
                "value": values["fluid"],
                "static": values["value"],
                "type": "spacing.fluid",
                "description": f"Spacing size {size}"
            }
        
        # Border radius
        radius_scale = {
            "none": {"value": "0", "description": "No border radius"},
            "sm": {"value": "0.125rem", "description": "Small border radius"},
            "md": {"value": "0.375rem", "description": "Medium border radius"},
            "lg": {"value": "0.5rem", "description": "Large border radius"},
            "xl": {"value": "0.75rem", "description": "Extra large border radius"},
            "full": {"value": "9999px", "description": "Full border radius"}
        }
        
        for size, config in radius_scale.items():
            tokens["designSystem"]["radius"]["scale"][size] = {
                "value": config["value"],
                "type": "borderRadius",
                "description": config["description"]
            }
        
        return tokens
    
    def _create_format_readme(self, format_dir: Path, tokens: dict):
        """Create format-specific README with usage instructions"""
        readme_content = f"""# Design Tokens Format Usage

This directory contains the extracted styles as design tokens in Style Dictionary format.

## Files
- `design-tokens.json` - Complete design system tokens in Style Dictionary format

## About Design Tokens

Design tokens are the visual design atoms of a design system — specifically, they are named entities that store visual design attributes. They're used in place of hard-coded values to maintain a scalable and consistent visual system.

## Style Dictionary Integration

This output is compatible with [Style Dictionary](https://amzn.github.io/style-dictionary/), Amazon's build system for design tokens.

### Installation
```bash
npm install -g style-dictionary
# or
npm install style-dictionary --save-dev
```

### Basic Configuration
Create a `style-dictionary.config.js` file:

```javascript
module.exports = {{
  "source": ["design-tokens/design-tokens.json"],
  "platforms": {{
    "css": {{
      "transformGroup": "css",
      "buildPath": "dist/css/",
      "files": [
        {{
          "destination": "variables.css",
          "format": "css/variables"
        }}
      ]
    }},
    "js": {{
      "transformGroup": "js",
      "buildPath": "dist/js/",
      "files": [
        {{
          "destination": "tokens.js",
          "format": "javascript/es6"
        }}
      ]
    }},
    "json": {{
      "transformGroup": "js",
      "buildPath": "dist/json/",
      "files": [
        {{
          "destination": "tokens.json",
          "format": "json/flat"
        }}
      ]
    }}
  }}
}}
```

### Build Tokens
```bash
# Build all platforms
style-dictionary build

# Build specific platform
style-dictionary build --platform css
```

## Platform Outputs

### CSS Variables
Generated CSS file with custom properties:

```css
:root {{
  --design-system-colors-semantic-primary: #ff0000;
  --design-system-typography-font-sizes-base: clamp(1rem, 2.5vw, 1.125rem);
  --design-system-spacing-scale-md: clamp(1rem, 3vw, 1.5rem);
}}
```

### JavaScript/TypeScript
Generated JavaScript module:

```javascript
export const designSystemColorsSemanticPrimary = '#ff0000';
export const designSystemTypographyFontSizesBase = 'clamp(1rem, 2.5vw, 1.125rem)';
export const designSystemSpacingScaleMd = 'clamp(1rem, 3vw, 1.5rem)';
```

### JSON
Flattened token structure:

```json
{{
  "design-system-colors-semantic-primary": "#ff0000",
  "design-system-typography-font-sizes-base": "clamp(1rem, 2.5vw, 1.125rem)",
  "design-system-spacing-scale-md": "clamp(1rem, 3vw, 1.5rem)"
}}
```

### React Native
Generate platform-specific tokens:

```javascript
module.exports = {{
  "platforms": {{
    "react-native": {{
      "transformGroup": "react-native",
      "buildPath": "dist/react-native/",
      "files": [
        {{
          "destination": "tokens.js",
          "format": "javascript/es6"
        }}
      ]
    }}
  }}
}}
```

## Advanced Configuration

### Custom Transforms
```javascript
// style-dictionary.config.js
const StyleDictionary = require('style-dictionary');

// Register custom transform
StyleDictionary.registerTransform({{
  name: 'size/fluid',
  type: 'value',
  matcher: function(token) {{
    return token.type === 'fontSize.fluid' || token.type === 'spacing.fluid';
  }},
  transformer: function(token) {{
    return token.value; // Keep fluid values as-is
  }}
}});

module.exports = {{
  // ... rest of config
  "platforms": {{
    "css": {{
      "transforms": [
        "attribute/cti",
        "name/cti/kebab",
        "size/fluid",
        "color/css"
      ],
      // ... rest of platform config
    }}
  }}
}}
```

### Custom Formats
```javascript
StyleDictionary.registerFormat({{
  name: 'css/custom-properties',
  formatter: function(dictionary) {{
    return `:root {{\n${{dictionary.allTokens.map(token => `  --${{token.name}}: ${{token.value}};`).join('\n')}}\n}}`;
  }}
}});
```

## Framework Integration

### React
```jsx
import {{ designSystemColorsSemanticPrimary, designSystemSpacingScaleMd }} from './dist/js/tokens.js';

function Button({{ children }}) {{
  return (
    <button style={{{{
      backgroundColor: designSystemColorsSemanticPrimary,
      padding: designSystemSpacingScaleMd,
    }}}>
      {{children}}
    </button>
  );
}}
```

### Vue
```vue
<template>
  <button :style="buttonStyles">{{{{ text }}}}</button>
</template>

<script>
import tokens from './dist/js/tokens.js';

export default {{
  computed: {{
    buttonStyles() {{
      return {{
        backgroundColor: tokens.designSystemColorsSemanticPrimary,
        padding: tokens.designSystemSpacingScaleMd,
      }};
    }}
  }}
}}
</script>
```

### Angular
```typescript
// tokens.service.ts
import {{ Injectable }} from '@angular/core';
import * as tokens from './dist/js/tokens.js';

@Injectable({{ providedIn: 'root' }})
export class TokensService {{
  getToken(path: string): string {{
    return tokens[path] || '';
  }}
}}
```

### Sass/SCSS
```scss
// Import generated Sass variables
@import 'dist/scss/variables';

.my-component {{
  background-color: $design-system-colors-semantic-primary;
  padding: $design-system-spacing-scale-md;
  font-size: $design-system-typography-font-sizes-base;
}}
```

## Multi-Platform Workflows

### Mobile Apps
```javascript
// iOS Swift
module.exports = {{
  "platforms": {{
    "ios-swift": {{
      "transformGroup": "ios-swift",
      "buildPath": "dist/ios/",
      "files": [
        {{
          "destination": "Tokens.swift",
          "format": "ios-swift/class.swift",
          "className": "DesignTokens"
        }}
      ]
    }}
  }}
}}

// Android Compose
"android-compose": {{
  "transformGroup": "compose",
  "buildPath": "dist/android/",
  "files": [
    {{
      "destination": "Tokens.kt",
      "format": "compose/object"
    }}
  ]
}}
```

### Design Tools
```javascript
// Figma Tokens
"figma": {{
  "transformGroup": "js",
  "buildPath": "dist/figma/",
  "files": [
    {{
      "destination": "figma-tokens.json",
      "format": "json/figma"
    }}
  ]
}}
```

## Token Categories

### Colors
- **Semantic:** Primary, secondary, background colors
- **Brand:** Extracted color palette from the website
- **Neutral:** Grayscale and neutral tones

### Typography
- **Font Families:** Primary, secondary, display fonts
- **Font Sizes:** Responsive/fluid sizing with clamp()
- **Font Weights:** Light to bold weight scale
- **Line Heights:** Tight to relaxed line height scale

### Spacing
- **Scale:** Consistent spacing system with fluid sizing
- **Responsive:** Values that adapt to screen size

### Border Radius
- **Scale:** From none to full radius options
- **Consistent:** Unified rounding across components

## Validation and Testing

### Token Validation
```javascript
// Add validation in config
module.exports = {{
  // ... other config
  "log": "verbose",
  "transform": {{
    "size/fluid": {{
      "type": "value",
      "matcher": function(token) {{
        return token.type === 'fontSize.fluid';
      }},
      "transformer": function(token) {{
        // Validate clamp() syntax
        if (!token.value.startsWith('clamp(')) {{
          throw new Error(`Invalid fluid value: ${{token.value}}`);
        }}
        return token.value;
      }}
    }}
  }}
}}
```

### Testing Outputs
```bash
# Test build
npm run build-tokens

# Validate CSS output
css-validator dist/css/variables.css

# Test JavaScript imports
node -e "console.log(require('./dist/js/tokens.js'))"
```

## Continuous Integration

### GitHub Actions
```yaml
name: Build Design Tokens
on: [push, pull_request]

jobs:
  build-tokens:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '16'
      - run: npm install
      - run: npm run build-tokens
      - run: npm run validate-tokens
```

## Documentation

The generated tokens include comprehensive metadata:
- **Type:** Token category (color, fontSize, spacing, etc.)
- **Description:** Human-readable description
- **Value:** The actual token value
- **Static:** Non-responsive fallback values where applicable

This enables automatic documentation generation and design system maintenance.

Generated by Web Style Extractor"""
        
        readme_path = format_dir / 'README.md'
        readme_path.write_text(readme_content, encoding='utf-8')


def get_generator():
    return DesignTokensGeneratorPlugin()