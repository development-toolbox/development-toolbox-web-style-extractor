"""
Font extraction plugin - extracts typography and font information
"""
import re
import logging
import tinycss2
import requests
from urllib.parse import urljoin
from plugins.base_plugin import BaseExtractor
from typing import List, Dict, Any


class FontExtractor(BaseExtractor):
    @property
    def name(self):
        return "font_extractor"
    
    @property
    def description(self):
        return "Extracts typography and font information"
    
    def extract(self, soup, driver, url: str) -> Dict[str, Any]:
        """Extract font and typography information"""
        
        # Get CSS text from the page
        css_text = self._get_css_text(soup, url)
        
        # Extract fonts using existing logic
        fonts = self._extract_fonts(css_text)
        
        # Get computed font styles if WebDriver is available
        computed_fonts = []
        if driver:
            try:
                computed_fonts = self._get_computed_fonts(driver)
            except Exception as e:
                logging.warning(f"Could not get computed fonts: {e}")
        
        # Analyze Google Fonts
        google_fonts = self._extract_google_fonts(soup, css_text)
        
        # Analyze typography scale
        typography_scale = self._analyze_typography_scale(driver) if driver else {}
        
        # Create font categories
        font_categories = self._categorize_fonts(fonts + computed_fonts)
        
        return {
            'fonts': list(set(fonts + computed_fonts))[:10],  # Top 10 unique fonts
            'primary_font': fonts[0] if fonts else None,
            'google_fonts': google_fonts,
            'typography_scale': typography_scale,
            'font_categories': font_categories,
            'css_fonts': fonts,
            'computed_fonts': computed_fonts,
            'total_fonts_found': len(set(fonts + computed_fonts))
        }
    
    def _get_css_text(self, soup, url: str) -> str:
        """Extract CSS text from page"""
        css_text = ""
        
        # Extract inline styles
        for element in soup.find_all(style=True):
            css_text += element.get('style', '') + ' '
        
        # Extract style tags
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                css_text += style_tag.string + ' '
        
        # Extract external stylesheets (first few)
        for link in soup.find_all('link', rel='stylesheet')[:5]:
            href = link.get('href')
            if href:
                try:
                    if not href.startswith(('http', '//')):
                        href = urljoin(url, href)
                    elif href.startswith('//'):
                        href = f"https:{href}"
                    
                    response = requests.get(href, timeout=5)
                    response.raise_for_status()
                    css_text += response.text + ' '
                except Exception as e:
                    logging.debug(f"Could not fetch CSS from {href}: {e}")
        
        return css_text
    
    def _extract_fonts(self, css_text: str) -> List[str]:
        """Extract font families from CSS text"""
        fonts = []
        
        try:
            # First try with tinycss2 for proper parsing
            rules = tinycss2.parse_stylesheet(css_text)
            for rule in rules:
                if rule.type == 'qualified-rule':
                    declarations = tinycss2.parse_declaration_list(rule.content)
                    for declaration in declarations:
                        if declaration.type == 'declaration' and declaration.name == 'font-family':
                            font_value = tinycss2.serialize(declaration.value).strip()
                            font_list = [f.strip().strip('"\'') for f in font_value.split(',')]
                            fonts.extend(font_list)
        except Exception:
            # Fallback to regex parsing
            font_pattern = r'font-family\s*:\s*([^;]+)'
            matches = re.findall(font_pattern, css_text, re.IGNORECASE)
            for match in matches:
                font_list = [f.strip().strip('"\'') for f in match.split(',')]
                fonts.extend(font_list)
        
        # Also check font shorthand properties
        font_shorthand_pattern = r'font\s*:\s*[^;]*?([\'"]?[A-Za-z][A-Za-z0-9\s\-]+[\'"]?)'
        shorthand_matches = re.findall(font_shorthand_pattern, css_text, re.IGNORECASE)
        for match in shorthand_matches:
            clean_font = match.strip().strip('"\'')
            if clean_font and not any(keyword in clean_font.lower() 
                                    for keyword in ['bold', 'italic', 'normal', 'px', 'em', 'rem']):
                fonts.append(clean_font)
        
        # Deduplicate and filter
        seen = set()
        unique_fonts = []
        for font in fonts:
            if font and font.lower() not in seen and len(font) > 1:
                seen.add(font.lower())
                unique_fonts.append(font)
        
        return unique_fonts[:10]  # Return top 10 fonts
    
    def _extract_google_fonts(self, soup, css_text: str) -> List[Dict[str, Any]]:
        """Extract Google Fonts being used"""
        google_fonts = []
        
        # Check for Google Fonts links
        google_font_links = soup.find_all('link', href=lambda x: x and 'fonts.googleapis.com' in x)
        
        for link in google_font_links:
            href = link.get('href', '')
            
            # Extract family names from the URL
            if 'family=' in href:
                family_part = href.split('family=')[1].split('&')[0]
                families = family_part.split('|')
                
                for family in families:
                    # Clean up the family name
                    clean_family = family.replace('+', ' ').split(':')[0]
                    
                    # Extract weights if specified
                    weights = []
                    if ':' in family:
                        weight_part = family.split(':')[1]
                        weights = weight_part.split(',')
                    
                    google_fonts.append({
                        'family': clean_family,
                        'weights': weights,
                        'url': href
                    })
        
        # Also check for @import statements in CSS
        import_pattern = r'@import\s+url\([\'"]?([^\'")]*fonts\.googleapis\.com[^\'")]*)[\'"]?\)'
        imports = re.findall(import_pattern, css_text)
        
        for import_url in imports:
            if 'family=' in import_url:
                family_part = import_url.split('family=')[1].split('&')[0]
                families = family_part.split('|')
                
                for family in families:
                    clean_family = family.replace('+', ' ').split(':')[0]
                    google_fonts.append({
                        'family': clean_family,
                        'weights': [],
                        'url': import_url
                    })
        
        return google_fonts
    
    def _get_computed_fonts(self, driver) -> List[str]:
        """Get fonts from computed styles using WebDriver"""
        try:
            script = """
            var fonts = [];
            var elements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, div, span, a, li');
            
            for (var i = 0; i < Math.min(elements.length, 50); i++) {
                var el = elements[i];
                var style = window.getComputedStyle(el);
                var fontFamily = style.fontFamily;
                
                if (fontFamily && fontFamily !== 'inherit') {
                    fonts.push(fontFamily);
                }
            }
            
            return fonts;
            """
            
            computed_fonts = driver.execute_script(script)
            return self._parse_computed_fonts(computed_fonts)
        except Exception as e:
            logging.debug(f"Could not get computed fonts: {e}")
            return []
    
    def _parse_computed_fonts(self, font_families: List[str]) -> List[str]:
        """Parse computed font-family values"""
        fonts = []
        
        for family_string in font_families:
            if family_string:
                # Split by comma and clean up each font
                family_list = [f.strip().strip('"\'') for f in family_string.split(',')]
                fonts.extend(family_list)
        
        # Deduplicate
        seen = set()
        unique_fonts = []
        for font in fonts:
            if font and font.lower() not in seen and len(font) > 1:
                seen.add(font.lower())
                unique_fonts.append(font)
        
        return unique_fonts
    
    def _analyze_typography_scale(self, driver) -> Dict[str, Any]:
        """Analyze typography hierarchy and scale"""
        try:
            script = """
            var typography = {
                headings: {},
                paragraphs: {},
                scale: []
            };
            
            // Analyze headings
            for (var i = 1; i <= 6; i++) {
                var heading = document.querySelector('h' + i);
                if (heading) {
                    var style = window.getComputedStyle(heading);
                    typography.headings['h' + i] = {
                        fontSize: style.fontSize,
                        fontWeight: style.fontWeight,
                        lineHeight: style.lineHeight,
                        fontFamily: style.fontFamily
                    };
                }
            }
            
            // Analyze paragraphs
            var p = document.querySelector('p');
            if (p) {
                var pStyle = window.getComputedStyle(p);
                typography.paragraphs.p = {
                    fontSize: pStyle.fontSize,
                    fontWeight: pStyle.fontWeight,
                    lineHeight: pStyle.lineHeight,
                    fontFamily: pStyle.fontFamily
                };
            }
            
            // Find all unique font sizes
            var elements = document.querySelectorAll('*');
            var sizes = new Set();
            
            for (var i = 0; i < Math.min(elements.length, 100); i++) {
                var el = elements[i];
                var style = window.getComputedStyle(el);
                var fontSize = style.fontSize;
                
                if (fontSize && fontSize !== '0px') {
                    sizes.add(fontSize);
                }
            }
            
            typography.scale = Array.from(sizes).sort(function(a, b) {
                return parseFloat(b) - parseFloat(a);
            }).slice(0, 10);
            
            return typography;
            """
            
            return driver.execute_script(script)
        except Exception as e:
            logging.debug(f"Could not analyze typography scale: {e}")
            return {}
    
    def _categorize_fonts(self, fonts: List[str]) -> Dict[str, List[str]]:
        """Categorize fonts by type"""
        categories = {
            'serif': [],
            'sans_serif': [],
            'monospace': [],
            'display': [],
            'system': [],
            'web_fonts': []
        }
        
        # Known font classifications
        serif_fonts = {'times', 'georgia', 'garamond', 'baskerville', 'minion'}
        sans_serif_fonts = {'arial', 'helvetica', 'verdana', 'calibri', 'open sans', 'roboto', 'lato'}
        monospace_fonts = {'courier', 'monaco', 'consolas', 'menlo', 'source code pro'}
        system_fonts = {'system-ui', '-apple-system', 'blinkmacsystemfont', 'segoe ui'}
        
        for font in fonts:
            font_lower = font.lower()
            
            if any(sf in font_lower for sf in serif_fonts) or 'serif' in font_lower:
                categories['serif'].append(font)
            elif any(ssf in font_lower for ssf in sans_serif_fonts) or 'sans' in font_lower:
                categories['sans_serif'].append(font)
            elif any(mf in font_lower for mf in monospace_fonts) or 'mono' in font_lower:
                categories['monospace'].append(font)
            elif any(sys in font_lower for sys in system_fonts):
                categories['system'].append(font)
            elif len(font.split()) > 1 and not any(keyword in font_lower for keyword in ['serif', 'sans', 'mono']):
                categories['web_fonts'].append(font)  # Likely a web font
            else:
                categories['display'].append(font)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}


def get_extractor():
    return FontExtractor()