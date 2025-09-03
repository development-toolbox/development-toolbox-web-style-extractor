"""
Design Tokens Generator Plugin
Generates Style Dictionary compatible design tokens
"""
import os
import json
import logging
from pathlib import Path
from plugins.base_plugin import BaseGenerator
from typing import Dict, Any


class DesignTokensGeneratorPlugin(BaseGenerator):
    """Generates Style Dictionary compatible design tokens"""
    
    @property
    def name(self) -> str:
        return "Design Tokens Generator"
    
    @property
    def output_format(self) -> str:
        return "design-tokens"
    
    @property
    def description(self) -> str:
        return "Style Dictionary compatible design tokens for multi-platform design systems"
    
    @property
    def emoji(self) -> str:
        return "🎨"
        
    @property
    def short_description(self) -> str:
        return "Multi-platform design tokens with Style Dictionary"
        
    @property
    def file_extension(self) -> str:
        return "json"
    
    @property
    def capabilities(self) -> list:
        return [
            'Multi-platform token generation',
            'Style Dictionary integration',
            'Semantic token naming',
            'Cross-platform compatibility',
            'Design system scaling'
        ]
    
    @property
    def use_cases(self) -> list:
        return [
            'Design system implementation',
            'Multi-platform applications',
            'Brand consistency',
            'Scalable design tokens'
        ]
    
    def generate(self, extraction_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
        """Generate Style Dictionary compatible design tokens"""
        try:
            if not output_path:
                return {'success': False, 'error': 'Output path required'}
            
            # Create format-specific directory
            format_dir = Path(output_path) / 'design-tokens'
            format_dir.mkdir(exist_ok=True)
            
            tokens_path = format_dir / 'design-tokens.json'
            
            # Archive existing file if it exists
            if tokens_path.exists():
                self.archive_existing_file(tokens_path, format_dir)
            
            # Generate tokens
            tokens = self._generate_tokens(extraction_data)
            
            # Write tokens file
            with open(tokens_path, 'w', encoding='utf-8') as f:
                json.dump(tokens, f, indent=2, ensure_ascii=False)
            
            # Create format-specific README
            self._create_format_readme(format_dir, tokens)
            
            logging.info(f"✅ Design tokens generated: {tokens_path}")
            
            return {
                'success': True,
                'file': str(tokens_path),
                'format': self.output_format,
                'content': tokens
            }
                
        except Exception as e:
            logging.error(f"Design tokens generation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _generate_tokens(self, extraction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Style Dictionary compatible tokens"""
        
        # Get extraction results
        extraction_results = extraction_data.get('extraction', {})
        color_data = extraction_results.get('color_extractor', {})
        font_data = extraction_results.get('font_extractor', {})
        
        colors = color_data.get('colors', [])
        fonts = font_data.get('fonts', [])
        
        tokens = {
            "color": {
                "semantic": {},
                "palette": {}
            },
            "font": {
                "family": {},
                "size": {},
                "weight": {}
            },
            "spacing": {
                "scale": {}
            },
            "border": {
                "radius": {}
            },
            "shadow": {}
        }
        
        # Process colors into semantic tokens
        if colors:
            tokens["color"]["semantic"] = {
                "primary": {"value": colors[0] if len(colors) > 0 else "#3b82f6"},
                "secondary": {"value": colors[1] if len(colors) > 1 else "#64748b"},
                "accent": {"value": colors[2] if len(colors) > 2 else "#06d6a0"},
                "success": {"value": colors[3] if len(colors) > 3 else "#10b981"},
                "warning": {"value": colors[4] if len(colors) > 4 else "#f59e0b"},
                "error": {"value": colors[5] if len(colors) > 5 else "#ef4444"}
            }
            
            # Add full palette
            for i, color in enumerate(colors[:20]):
                tokens["color"]["palette"][f"color-{i+1}"] = {"value": color}
        
        # Process fonts
        valid_fonts = [f for f in fonts if not f.startswith('var(') and f not in ['inherit', 'initial']]
        
        if valid_fonts:
            tokens["font"]["family"] = {
                "primary": {"value": [valid_fonts[0], "system-ui", "sans-serif"]},
                "secondary": {"value": [valid_fonts[1], "system-ui", "sans-serif"] if len(valid_fonts) > 1 else ["system-ui", "sans-serif"]},
                "monospace": {"value": ["SFMono-Regular", "Menlo", "Monaco", "Consolas", "monospace"]}
            }
        
        # Add typography scale
        tokens["font"]["size"] = {
            "xs": {"value": "12px"},
            "sm": {"value": "14px"},
            "base": {"value": "16px"},
            "lg": {"value": "18px"},
            "xl": {"value": "20px"},
            "2xl": {"value": "24px"},
            "3xl": {"value": "30px"},
            "4xl": {"value": "36px"}
        }
        
        tokens["font"]["weight"] = {
            "light": {"value": "300"},
            "normal": {"value": "400"},
            "medium": {"value": "500"},
            "semibold": {"value": "600"},
            "bold": {"value": "700"}
        }
        
        # Add spacing scale
        tokens["spacing"]["scale"] = {
            "xs": {"value": "4px"},
            "sm": {"value": "8px"},
            "md": {"value": "16px"},
            "lg": {"value": "24px"},
            "xl": {"value": "32px"},
            "2xl": {"value": "48px"},
            "3xl": {"value": "64px"}
        }
        
        # Add border radius
        tokens["border"]["radius"] = {
            "none": {"value": "0px"},
            "sm": {"value": "4px"},
            "base": {"value": "8px"},
            "lg": {"value": "12px"},
            "xl": {"value": "16px"},
            "full": {"value": "9999px"}
        }
        
        # Add shadows
        tokens["shadow"] = {
            "sm": {"value": "0 1px 2px 0 rgb(0 0 0 / 0.05)"},
            "base": {"value": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)"},
            "md": {"value": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)"},
            "lg": {"value": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"}
        }
        
        return tokens
    
    def _create_format_readme(self, format_dir: Path, tokens: dict):
        """Create format-specific README with usage instructions"""
        readme_content = f"""# Design Tokens Usage

This directory contains extracted styles as Style Dictionary compatible design tokens.

## Files
- `design-tokens.json` - Complete design token definitions for multi-platform use

## Installation & Setup

### 1. Install Style Dictionary
```bash
npm install -D style-dictionary
# or
yarn add -D style-dictionary
```

### 2. Configure Style Dictionary
Create `build.js` or add to your build process:

```javascript
const StyleDictionary = require('style-dictionary');

// Configure platforms
StyleDictionary.extend({{
  source: ['design-tokens.json'],
  platforms: {{
    css: {{
      transformGroup: 'css',
      buildPath: 'dist/css/',
      files: [{{
        destination: 'tokens.css',
        format: 'css/variables'
      }}]
    }},
    js: {{
      transformGroup: 'js',
      buildPath: 'dist/js/',
      files: [{{
        destination: 'tokens.js',
        format: 'javascript/es6'
      }}]
    }},
    ios: {{
      transformGroup: 'ios',
      buildPath: 'dist/ios/',
      files: [{{
        destination: 'tokens.h',
        format: 'ios/macros'
      }}]
    }},
    android: {{
      transformGroup: 'android',
      buildPath: 'dist/android/',
      files: [{{
        destination: 'tokens.xml',
        format: 'android/resources'
      }}]
    }}
  }}
}}).buildAllPlatforms();
```

### 3. Generate Platform Files
```bash
node build.js
```

## Usage Examples

### CSS Variables
```css
/* Generated from tokens */
:root {{
  --color-semantic-primary: #your-primary-color;
  --font-family-primary: 'Your Font', system-ui, sans-serif;
  --spacing-scale-md: 16px;
}}

.button {{
  background: var(--color-semantic-primary);
  font-family: var(--font-family-primary);
  padding: var(--spacing-scale-md);
}}
```

### JavaScript/TypeScript
```javascript
import {{ colorSemanticPrimary, spacingScaleMd }} from './dist/js/tokens.js';

const styles = {{
  backgroundColor: colorSemanticPrimary,
  padding: spacingScaleMd
}};
```

### React
```jsx
import {{ colorSemanticPrimary, spacingScaleMd }} from './dist/js/tokens.js';

function Button({{ children }}) {{
  return (
    <button style={{{{
      backgroundColor: colorSemanticPrimary,
      padding: spacingScaleMd,
    }}}}>
      {{children}}
    </button>
  );
}}
```

### Vue
```vue
<template>
  <button :style="buttonStyles">
    <slot />
  </button>
</template>

<script setup>
import {{ colorSemanticPrimary, spacingScaleMd }} from './dist/js/tokens.js';

const buttonStyles = {{
  backgroundColor: colorSemanticPrimary,
  padding: spacingScaleMd
}};
</script>
```

## Token Categories

### Colors
- **Semantic**: Primary, secondary, accent, success, warning, error
- **Palette**: Full extracted color palette (color-1, color-2, etc.)

### Typography
- **Families**: Primary, secondary, monospace font stacks
- **Sizes**: xs (12px) to 4xl (36px) scale
- **Weights**: Light (300) to bold (700)

### Spacing
- **Scale**: xs (4px) to 3xl (64px) consistent spacing system

### Borders & Shadows
- **Radius**: none to full (9999px) border radius options
- **Shadow**: sm to lg elevation system

## Multi-Platform Output

Style Dictionary can generate tokens for:
- **Web**: CSS variables, SCSS variables, JavaScript objects
- **iOS**: Objective-C macros, Swift constants, Plist files
- **Android**: XML resources, Kotlin objects
- **Flutter**: Dart constants
- **React Native**: JavaScript objects

## Documentation

- [Style Dictionary Documentation](https://amzn.github.io/style-dictionary/)
- [Token Naming Guidelines](https://amzn.github.io/style-dictionary/#/tokens)
- [Platform Configuration](https://amzn.github.io/style-dictionary/#/config)

Generated by Web Style Extractor"""
        
        readme_path = format_dir / 'README.md'
        readme_path.write_text(readme_content, encoding='utf-8')


def get_generator():
    return DesignTokensGeneratorPlugin()