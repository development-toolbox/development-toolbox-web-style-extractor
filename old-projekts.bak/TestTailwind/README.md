# 🎨 Style Guide for saab.com

**Extracted from:** [https://saab.com](https://saab.com)  
**Generated:** 2025-09-02 22:55:38  
**Format:** TAILWIND
**🚀 Web Style Extractor v2.0** - Complete Tailwind CSS configuration with extracted color palettes and font families

## 📊 Comprehensive Analysis

### 🎨 **Color System**
- **Colors Found:** 10 unique colors extracted
- **Modern Support:** All colors converted to OKLCH color space
- **Dynamic Variations:** Light/dark variants generated using CSS relative color syntax
- **Semantic Mapping:** Colors classified by usage (primary, secondary, background, text)

### 🔤 **Typography System** 
- **Fonts Found:** 5 font families detected
- **Font Classification:** Automatically categorized (serif, sans-serif, monospace, display)
- **Fluid Typography:** Responsive font sizing with clamp() functions generated
- **Font Stack Optimization:** Fallback-aware declarations created

### 🎯 **Key Style Properties**
- **Body Background:** `rgb(243, 243, 242)`
- **Primary Text:** `rgb(255, 255, 255)`
- **Link Colors:** `rgb(255, 255, 255)`
- **Font Family:** Optimized font stacks with fallbacks

## 📁 Project Structure

- **`styles.js`** - Complete Tailwind CSS configuration with extracted color palettes and font families
- **`metadata.txt`** - Comprehensive extraction details and analysis
- **`README.md`** - This documentation file  
- **`README.html`** - 🌟 **Interactive preview with live font rendering!**

## 🎨 Complete Color Palette

| # | Hex Code | OKLCH Equivalent | Visual Sample |
|---|----------|------------------|---------------|
| 1 | `#ffff00` | `oklch(50.0% 0.370 60.0deg)` | ![#ffff00](https://img.shields.io/badge/-ffff00-ffff00?style=flat-square) |
| 2 | `#000000` | `oklch(0.0% 0.000 0.0deg)` | ![#000000](https://img.shields.io/badge/-000000-000000?style=flat-square) |
| 3 | `#444444` | `oklch(26.7% 0.000 0.0deg)` | ![#444444](https://img.shields.io/badge/-444444-444444?style=flat-square) |
| 4 | `#999999` | `oklch(60.0% 0.000 0.0deg)` | ![#999999](https://img.shields.io/badge/-999999-999999?style=flat-square) |
| 5 | `#e6e6e6` | `oklch(90.2% 0.000 0.0deg)` | ![#e6e6e6](https://img.shields.io/badge/-e6e6e6-e6e6e6?style=flat-square) |
| 6 | `#0078e7` | `oklch(45.3% 0.370 208.8deg)` | ![#0078e7](https://img.shields.io/badge/-0078e7-0078e7?style=flat-square) |
| 7 | `#ffffff` | `oklch(100.0% 0.000 0.0deg)` | ![#ffffff](https://img.shields.io/badge/-ffffff-ffffff?style=flat-square) |
| 8 | `#cccccc` | `oklch(80.0% 0.000 0.0deg)` | ![#cccccc](https://img.shields.io/badge/-cccccc-cccccc?style=flat-square) |
| 9 | `#dddddd` | `oklch(86.7% 0.000 0.0deg)` | ![#dddddd](https://img.shields.io/badge/-dddddd-dddddd?style=flat-square) |
| 10 | `#129fea` | `oklch(49.4% 0.317 200.8deg)` | ![#129fea](https://img.shields.io/badge/-129fea-129fea?style=flat-square) |

## 🔤 Font Analysis & Classification

| Font Family | Classification | Usage Context | Fallback Strategy |
|-------------|----------------|---------------|-------------------|
| `monospace` | **Monospace** 🔤 | Monospace/Code | `monospace, 'Courier New'` |
| `FreeSans` | **Custom** ✨ | Sans-serif Fallback | `sans-serif` *(generic)* |
| `Arimo` | **Custom** ✨ | Display/Custom | `sans-serif` *(generic)* |
| `Droid Sans` | **Custom** ✨ | Sans-serif Fallback | `sans-serif` *(generic)* |
| `Helvetica` | **Sans-serif** ✏️ | Display/Custom | `sans-serif` *(generic)* |

**💡 See Live Font Rendering:** Open `README.html` in your browser to see exactly how each font renders with real text samples!

## ⚡ Using Your Tailwind Config

### 📦 **Installation**
```bash
# Replace your tailwind.config.js with the generated file
cp styles.js tailwind.config.js

# Or merge with existing config
```

### 🎨 **Using Extracted Colors**
```html
<!-- Use extracted color palettes -->
<div class="bg-primary-500 text-primary-50">
  Styled with extracted GitHub colors!
</div>

<!-- Custom color utilities -->
<div class="bg-color-3 text-color-1">
  Direct color usage
</div>
```

### 🔤 **Typography Classes**
```html
<!-- Use detected font families -->
<h1 class="font-sans text-fluid-xl">
  Rendered with extracted fonts
</h1>
```

## 🚀 Advanced Features Available

### 🎨 **Modern CSS Output** (`--output modern-css`)
- **OKLCH Color Space**: Future-proof color definitions with better perceptual uniformity
- **Container Queries**: Modern responsive design patterns that respond to container size
- **CSS Nesting**: Native CSS nesting without preprocessors
- **Fluid Typography**: Responsive text scaling using clamp() functions
- **Dynamic Color Variations**: CSS relative color syntax for automatic light/dark variants

### ⚡ **Tailwind Configuration** (`--output tailwind`)
- **Custom Color Palettes**: Extracted colors mapped to Tailwind color scales
- **Font Family Integration**: Detected fonts configured as Tailwind font families
- **Spacing System**: Consistent spacing tokens derived from the design
- **Component-Ready**: Drop into any Tailwind project immediately

### 🎯 **Design Tokens** (`--output design-tokens`)
- **Style Dictionary Compatible**: JSON format ready for multi-platform generation
- **Semantic Color Mapping**: Meaningful color names (primary, secondary, background, text)
- **Typography Scale**: Fluid font sizing with both relative and static values
- **Component Tokens**: Button, input, and common component styling variables

## 🔧 Developer Integration

### 📦 **Import into Your Project**
```bash
# Copy the generated file to your project
cp styles.js src/styles/

# For Tailwind projects
cp styles.js tailwind.config.js

# For Design System projects  
cp styles.json tokens/design-tokens.json
```

### 🎨 **Use in Your CSS**
```css
/* Import generated variables */
@import 'styles.css';

/* Use extracted colors */
.my-component {
  background: var(--color-primary);
  color: var(--color-text-primary);
  font-family: var(--font-primary);
}
```

### ⚛️ **React/Vue Integration**
```javascript
// Import design tokens
import tokens from './styles.json';

// Use in your components
const MyComponent = () => (
  <div style={{
    backgroundColor: tokens.designSystem.colors.semantic.background.value,
    color: tokens.designSystem.colors.semantic['text-primary'].value
  }}>
    Styled with extracted design tokens!
  </div>
);
```

## 📚 Learn More

### 🔗 **Documentation Links**
- **[Web Style Extractor v2.0 Documentation](../../../README.md)** - Complete feature guide
- **[Modern CSS Features Guide](../../../web-style-extractor-modern-features.md)** - Latest CSS capabilities
- **[MediaWiki Templates](../../../docs/mediawiki-usage.md)** - Wiki integration guide
- **[Design Token Usage](../../../docs/design-tokens.md)** - Style Dictionary workflows

### 🎯 **Next Steps**
1. **Review the extracted styles** in `README.html` for visual validation
2. **Choose your output format** based on your project needs
3. **Integrate the generated code** into your development workflow
4. **Customize and extend** the extracted design system as needed

---

**🚀 Generated by Web Style Extractor v2.0** - The industry-leading CSS analysis tool for modern web development  
✨ **Modern Features:** OKLCH colors • Design tokens • Tailwind configs • Container queries • Fluid typography
