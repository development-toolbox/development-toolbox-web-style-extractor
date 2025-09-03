"""
README Generator Plugin
Creates intelligent project documentation (README.md + README.html) with archive system
"""
import os
import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from plugins.base_plugin import BaseGenerator


class ReadmeGeneratorPlugin(BaseGenerator):
    """Generates intelligent project READMEs with archiving support"""
    
    @property
    def name(self) -> str:
        return "README Generator"
    
    @property
    def output_format(self) -> str:
        return "readme"
    
    @property
    def description(self) -> str:
        return "Comprehensive project documentation with live previews and format guides"
    
    @property
    def emoji(self) -> str:
        return "📚"
        
    @property
    def short_description(self) -> str:
        return "Project documentation with intelligent archiving"
        
    @property
    def file_extension(self) -> str:
        return "md"  # Primary extension, also creates .html
    
    @property
    def capabilities(self) -> list:
        return [
            'Multi-format documentation',
            'Live font previews',
            'Interactive HTML reports',
            'Intelligent archiving',
            'Format usage guides'
        ]
    
    @property
    def use_cases(self) -> list:
        return [
            'Project documentation',
            'Design system overview',
            'Client deliverables',
            'Development handoff'
        ]
    
    def generate(self, extraction_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
        """Generate project READMEs with intelligent file management"""
        try:
            if not output_path:
                return {'success': False, 'error': 'Output path required for README generation'}
            
            project_path = Path(output_path)
            
            # Scan existing files to understand what formats are present
            existing_formats = self._scan_existing_formats(project_path)
            
            # Generate README.md
            readme_md = self._generate_readme_md(extraction_data, existing_formats, project_path)
            readme_md_path = project_path / "README.md"
            
            # Generate README.html  
            readme_html = self._generate_readme_html(extraction_data, existing_formats, project_path)
            readme_html_path = project_path / "README.html"
            
            # Archive existing README files if they exist (special case - archive in project root)
            if readme_md_path.exists() or readme_html_path.exists():
                self._archive_readme_files(project_path)
            
            # Write files
            readme_md_path.write_text(readme_md, encoding='utf-8')
            readme_html_path.write_text(readme_html, encoding='utf-8')
            
            logging.info(f"✅ README files generated: {readme_md_path}, {readme_html_path}")
            
            return {
                'success': True,
                'files': [str(readme_md_path), str(readme_html_path)],
                'format': self.output_format,
                'existing_formats': existing_formats,
                'archived': readme_md_path.exists() or readme_html_path.exists()
            }
                
        except Exception as e:
            logging.error(f"README generation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _scan_existing_formats(self, project_path: Path) -> List[str]:
        """Scan project directory for existing format folders"""
        formats = []
        
        # Check for format directories with their expected files
        format_patterns = {
            'json': 'json/styles.json',
            'mediawiki': 'mediawiki/styles.mediawiki',
            'tailwind': 'tailwind/tailwind.config.js',
            'css': 'css/styles.css',
            'modern-css': 'modern-css/styles.css',
            'design-tokens': 'design-tokens/design-tokens.json',
            'bookstack': 'bookstack/custom.css',
            'html': 'html/styles.html'
        }
        
        for format_name, file_pattern in format_patterns.items():
            file_path = project_path / file_pattern
            if file_path.exists():
                formats.append(format_name)
        
        return formats
    
    
    def _generate_readme_md(self, extraction_data: Dict[str, Any], existing_formats: List[str], project_path: Path) -> str:
        """Generate comprehensive README.md content"""
        
        # Get basic info
        url = extraction_data.get('url', 'Unknown URL')
        timestamp = extraction_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Get color and font data (corrected structure)
        extraction_results = extraction_data.get('extraction', {})
        color_data = extraction_results.get('color_extractor', {})
        font_data = extraction_results.get('font_extractor', {})
        colors = color_data.get('colors', [])
        fonts = font_data.get('fonts', [])
        
        # Build format list
        format_list = ""
        if existing_formats:
            for fmt in existing_formats:
                format_list += f"- **{fmt.upper()}** - `{self._get_format_filename(fmt)}`\n"
        else:
            format_list = "- No format files detected in this generation\n"
        
        # Build color table
        color_table = ""
        if colors:
            color_table = "| # | Hex Code | Preview |\n|---|----------|----------|\n"
            for i, color in enumerate(colors[:20]):  # Limit to 20 colors
                color_table += f"| {i+1} | `{color}` | ![{color}](https://via.placeholder.com/20x20/{color.replace('#', '')}/{color.replace('#', '')}) |\n"
        else:
            color_table = "*No colors extracted*\n"
        
        # Build font list
        font_list = ""
        if fonts:
            for font in fonts[:10]:  # Limit to 10 fonts
                font_list += f"- `{font}`\n"
        else:
            font_list = "*No fonts extracted*\n"
        
        readme_content = f"""# Style Extraction Report

**Website:** {url}  
**Extracted:** {timestamp}  
**Project:** {project_path.name}

## 📁 Generated Files

{format_list}

## 🎨 Color Palette ({len(colors)} colors found)

{color_table}

## 🔤 Typography ({len(fonts)} fonts found)

{font_list}

## 📚 Documentation

- **[📖 README.html](./README.html)** - Interactive preview with live font rendering
- **[📊 metadata.txt](./metadata.txt)** - Detailed extraction analysis

### Format Guides

- [📖 **Complete Documentation**](../../docs/html/index.html) - All format guides
- [⚡ **Tailwind Guide**](../../docs/html/tailwind.html) - Tailwind CSS setup
- [🎨 **Design Tokens**](../../docs/html/design-tokens.html) - Style Dictionary usage
- [📝 **MediaWiki**](../../docs/html/mediawiki.html) - Wiki integration

## 🗂️ Archive History

Regenerated files are automatically archived in `archive/YYYY-MM-DD-HH-MM/` to preserve previous versions.

---

*Generated by Web Style Extractor - Advanced CSS analysis and extraction tool*
"""
        
        return readme_content
    
    def _generate_readme_html(self, extraction_data: Dict[str, Any], existing_formats: List[str], project_path: Path) -> str:
        """Generate interactive HTML README with live previews"""
        
        # Get data
        url = extraction_data.get('url', 'Unknown URL')
        timestamp = extraction_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Get color and font data (corrected structure)
        extraction_results = extraction_data.get('extraction', {})
        color_data = extraction_results.get('color_extractor', {})
        font_data = extraction_results.get('font_extractor', {})
        colors = color_data.get('colors', [])
        fonts = font_data.get('fonts', [])
        
        # Build color grid
        color_grid = ""
        if colors:
            for i, color in enumerate(colors[:24]):  # Limit to 24 colors for grid
                color_grid += f"""
                <div class="color-swatch" style="background-color: {color}">
                    <div class="color-info">
                        <div class="color-hex">{color}</div>
                    </div>
                </div>"""
        else:
            color_grid = "<p><em>No colors extracted</em></p>"
        
        # Build font previews (filter out CSS variables and invalid fonts)
        font_previews = ""
        if fonts:
            valid_fonts = self._filter_valid_fonts(fonts)
            for font in valid_fonts[:8]:  # Limit to 8 valid fonts
                font_previews += f"""
                <div class="font-sample" style="font-family: {self._format_font_for_css(font)}, sans-serif">
                    <div class="font-name">{font}</div>
                    <div class="font-demo">The quick brown fox jumps over the lazy dog</div>
                    <div class="font-sizes">
                        <span style="font-size: 14px">14px</span>
                        <span style="font-size: 18px">18px</span>
                        <span style="font-size: 24px">24px</span>
                    </div>
                </div>"""
        else:
            font_previews = "<p><em>No fonts extracted</em></p>"
        
        # Build format files list
        format_files = ""
        if existing_formats:
            for fmt in existing_formats:
                filename = self._get_format_filename(fmt)
                format_files += f"""
                <li>
                    <strong>{fmt.upper()}</strong> - 
                    <code>{filename}</code>
                    <a href="../../docs/html/{fmt}.html" target="_blank">📖 Guide</a>
                </li>"""
        else:
            format_files = "<li><em>No format files in this generation</em></li>"
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Style Guide - {project_path.name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: #fafafa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{ color: #333; }}
        .meta {{ 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        .color-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin-bottom: 30px;
        }}
        .color-swatch {{
            aspect-ratio: 1;
            border-radius: 5px;
            display: flex;
            align-items: end;
            padding: 8px;
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
        }}
        .color-info {{
            background: rgba(0,0,0,0.6);
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 12px;
            width: 100%;
        }}
        .font-sample {{
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
        }}
        .font-name {{
            font-weight: bold;
            color: #666;
            font-size: 14px;
            margin-bottom: 5px;
        }}
        .font-demo {{
            font-size: 18px;
            margin-bottom: 10px;
        }}
        .font-sizes span {{
            margin-right: 15px;
            padding: 3px 8px;
            background: #f0f0f0;
            border-radius: 3px;
        }}
        .files-list {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
        }}
        .files-list ul {{
            margin: 0;
            padding-left: 20px;
        }}
        .files-list a {{
            margin-left: 10px;
            text-decoration: none;
            color: #007bff;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Style Extraction Report</h1>
        
        <div class="meta">
            <strong>Website:</strong> {url}<br>
            <strong>Extracted:</strong> {timestamp}<br>
            <strong>Project:</strong> {project_path.name}
        </div>
        
        <h2>📁 Generated Files</h2>
        <div class="files-list">
            <ul>
                {format_files}
            </ul>
        </div>
        
        <h2>🎨 Color Palette ({len(colors)} colors)</h2>
        <div class="color-grid">
            {color_grid}
        </div>
        
        <h2>🔤 Typography ({len(fonts)} fonts)</h2>
        <div class="font-previews">
            {font_previews}
        </div>
        
        <h2>📚 Documentation</h2>
        <ul>
            <li><a href="../../docs/html/index.html" target="_blank">📖 Complete Documentation</a></li>
            <li><a href="../../docs/html/tailwind.html" target="_blank">⚡ Tailwind CSS Guide</a></li>
            <li><a href="../../docs/html/design-tokens.html" target="_blank">🎨 Design Tokens Guide</a></li>
            <li><a href="../../docs/html/mediawiki.html" target="_blank">📝 MediaWiki Guide</a></li>
        </ul>
        
        <div class="footer">
            <p>Generated by <strong>Web Style Extractor</strong> - Advanced CSS analysis tool</p>
        </div>
    </div>
</body>
</html>"""
        
        return html_content
    
    def _get_format_filename(self, format_name: str) -> str:
        """Get the expected filename for a format"""
        format_files = {
            'json': 'json/styles.json',
            'mediawiki': 'mediawiki/styles.mediawiki',
            'tailwind': 'tailwind/tailwind.config.js',
            'css': 'css/styles.css',
            'modern-css': 'modern-css/styles.css',
            'design-tokens': 'design-tokens/design-tokens.json',
            'bookstack': 'bookstack/',
            'html': 'html/styles.html'
        }
        return format_files.get(format_name, f'{format_name}/styles.{format_name}')
    
    def _archive_readme_files(self, project_path: Path):
        """Archive existing README files with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        archive_path = project_path / "archive" / timestamp
        archive_path.mkdir(parents=True, exist_ok=True)
        
        files_to_archive = ["README.md", "README.html", "metadata.txt"]
        
        for file_name in files_to_archive:
            source = project_path / file_name
            if source.exists():
                dest = archive_path / file_name
                shutil.move(str(source), str(dest))
                logging.info(f"📦 Archived {file_name} to archive/{timestamp}/")
    
    def _filter_valid_fonts(self, fonts: List[str]) -> List[str]:
        """Filter out CSS variables and invalid font names"""
        valid_fonts = []
        invalid_patterns = [
            'var(',  # CSS variables
            'inherit',  # CSS keywords
            'initial',
            'unset',
            'none'
        ]
        
        for font in fonts:
            font_lower = font.lower()
            if not any(pattern in font_lower for pattern in invalid_patterns):
                if len(font) > 1 and not font.startswith('-'):  # Skip single chars and CSS prefixes
                    valid_fonts.append(font)
        
        return valid_fonts
    
    def _format_font_for_css(self, font: str) -> str:
        """Format font name properly for CSS"""
        # If font has spaces or special chars, quote it
        if ' ' in font or '-' in font:
            return f"'{font}'"
        return font


def get_generator():
    return ReadmeGeneratorPlugin()