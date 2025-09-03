"""
Color extraction plugin - extracts colors from CSS and computed styles
"""
import re
import logging
import requests
import io
from urllib.parse import urljoin
from PIL import Image, UnidentifiedImageError
from plugins.base_plugin import BaseExtractor
import bs4
from typing import List, Dict, Any


class ColorExtractor(BaseExtractor):
    @property
    def name(self):
        return "color_extractor"
    
    @property
    def description(self):
        return "Extracts colors from CSS and computed styles"
    
    def extract(self, soup, driver, url: str) -> Dict[str, Any]:
        """Extract colors from webpage"""
        
        # Get CSS text from the page
        css_text = self._get_css_text(soup, url)
        
        # Extract colors using existing logic
        colors = self._extract_colors(css_text, soup, url)
        
        # Get computed styles if WebDriver is available
        computed_colors = []
        if driver:
            try:
                computed_colors = self._get_computed_colors(driver)
            except Exception as e:
                logging.warning(f"Could not get computed colors: {e}")
        
        # Combine and deduplicate colors
        all_colors = list(set(colors + computed_colors))
        
        # Sort by frequency/importance
        sorted_colors = self._prioritize_colors(all_colors)
        
        # Generate color palette
        palette = self._generate_palette(sorted_colors[:10])
        
        return {
            'colors': sorted_colors[:20],  # Top 20 colors
            'primary_color': sorted_colors[0] if sorted_colors else None,
            'color_palette': palette,
            'total_colors_found': len(all_colors),
            'computed_colors': computed_colors,
            'css_colors': colors
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
    
    def _extract_colors(self, css_text: str, soup, url: str) -> List[str]:
        """Extract colors from CSS text"""
        hex_pattern = r'#(?:[0-9a-fA-F]{3,4}){1,2}\b'
        rgb_pattern = r'rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+(?:,\s*[\d.]+)?\)'
        
        hex_colors = re.findall(hex_pattern, css_text)
        rgb_colors = re.findall(rgb_pattern, css_text)
        
        normalized_colors = []
        
        # Normalize hex colors
        for color in hex_colors:
            if len(color) == 4:  # #abc -> #aabbcc
                color = f'#{color[1]}{color[1]}{color[2]}{color[2]}{color[3]}{color[3]}'
            normalized_colors.append(color.lower())
        
        # Convert RGB to hex
        for color in rgb_colors:
            numbers = list(map(int, re.findall(r'\d+', color)))
            if len(numbers) >= 3:
                hex_color = f'#{numbers[0]:02x}{numbers[1]:02x}{numbers[2]:02x}'
                normalized_colors.append(hex_color)
        
        # Try to extract colors from images
        image_colors = self._extract_image_colors(soup, url)
        normalized_colors.extend(image_colors)
        
        return normalized_colors
    
    def _extract_image_colors(self, soup, url: str) -> List[str]:
        """Extract dominant colors from the first image"""
        try:
            hero_image = soup.find('img')
            if isinstance(hero_image, bs4.element.Tag):
                img_src = hero_image.get('src')
                if img_src:
                    img_url = str(img_src)
                    if not img_url.startswith(('http', '//')):
                        img_url = urljoin(url, img_url)
                    elif img_url.startswith('//'):
                        img_url = f"https:{img_url}"
                    
                    return self._get_dominant_colors(img_url)
        except Exception as e:
            logging.debug(f"Could not extract image colors: {e}")
        
        return []
    
    def _get_dominant_colors(self, img_url: str) -> List[str]:
        """Get dominant colors from an image"""
        try:
            response = requests.get(img_url, timeout=5)
            response.raise_for_status()
            
            img = Image.open(io.BytesIO(response.content))
            img = img.convert('RGB')
            img = img.resize((50, 50))  # Reduce size for faster processing
            
            colors = img.getcolors(maxcolors=256)
            if colors:
                # Sort by frequency and convert to hex
                colors.sort(reverse=True, key=lambda x: x[0])
                hex_colors = []
                for count, (r, g, b) in colors[:5]:  # Top 5 colors
                    hex_color = f'#{r:02x}{g:02x}{b:02x}'
                    hex_colors.append(hex_color)
                return hex_colors
        except Exception as e:
            logging.debug(f"Could not process image {img_url}: {e}")
        
        return []
    
    def _get_computed_colors(self, driver) -> List[str]:
        """Get colors from computed styles using WebDriver"""
        try:
            script = """
            var colors = [];
            var elements = document.querySelectorAll('*');
            for (var i = 0; i < Math.min(elements.length, 100); i++) {
                var el = elements[i];
                var style = window.getComputedStyle(el);
                
                // Get various color properties
                var colorProps = ['color', 'backgroundColor', 'borderColor', 'outlineColor'];
                for (var j = 0; j < colorProps.length; j++) {
                    var color = style[colorProps[j]];
                    if (color && color !== 'rgba(0, 0, 0, 0)' && color !== 'transparent') {
                        colors.push(color);
                    }
                }
            }
            return colors;
            """
            
            computed_colors = driver.execute_script(script)
            return self._normalize_computed_colors(computed_colors)
        except Exception as e:
            logging.debug(f"Could not get computed colors: {e}")
            return []
    
    def _normalize_computed_colors(self, colors: List[str]) -> List[str]:
        """Convert computed colors to hex format"""
        normalized = []
        
        for color in colors:
            try:
                if color.startswith('rgb'):
                    # Parse rgb(r, g, b) or rgba(r, g, b, a)
                    numbers = re.findall(r'\d+', color)
                    if len(numbers) >= 3:
                        r, g, b = map(int, numbers[:3])
                        hex_color = f'#{r:02x}{g:02x}{b:02x}'
                        normalized.append(hex_color)
                elif color.startswith('#'):
                    normalized.append(color.lower())
            except Exception as e:
                logging.debug(f"Could not normalize color {color}: {e}")
        
        return normalized
    
    def _prioritize_colors(self, colors: List[str]) -> List[str]:
        """Sort colors by frequency and filter out common/boring colors"""
        # Count frequency
        color_counts = {}
        for color in colors:
            color_counts[color] = color_counts.get(color, 0) + 1
        
        # Filter out very common colors
        boring_colors = {
            '#000000', '#ffffff', '#fff', '#000',
            '#f0f0f0', '#e0e0e0', '#d0d0d0', '#c0c0c0',
            '#808080', '#404040', '#202020'
        }
        
        # Sort by frequency, exclude boring colors
        sorted_colors = sorted(
            [(count, color) for color, count in color_counts.items() 
             if color not in boring_colors],
            reverse=True
        )
        
        return [color for count, color in sorted_colors]
    
    def _generate_palette(self, colors: List[str]) -> Dict[str, Any]:
        """Generate color palette with variations"""
        if not colors:
            return {}
        
        palette = {
            'primary': colors[0] if len(colors) > 0 else None,
            'secondary': colors[1] if len(colors) > 1 else None,
            'accent': colors[2] if len(colors) > 2 else None,
            'background': self._find_background_color(colors),
            'text': self._find_text_color(colors),
            'all_colors': colors
        }
        
        # Generate variations for primary color
        if palette['primary']:
            palette['variations'] = {
                'light': self._lighten_color(palette['primary']),
                'dark': self._darken_color(palette['primary'])
            }
        
        return palette
    
    def _find_background_color(self, colors: List[str]) -> str:
        """Find most likely background color"""
        # Look for light colors that could be backgrounds
        light_colors = [c for c in colors if self._is_light_color(c)]
        return light_colors[0] if light_colors else '#ffffff'
    
    def _find_text_color(self, colors: List[str]) -> str:
        """Find most likely text color"""
        # Look for dark colors that could be text
        dark_colors = [c for c in colors if not self._is_light_color(c)]
        return dark_colors[0] if dark_colors else '#000000'
    
    def _is_light_color(self, hex_color: str) -> bool:
        """Check if a color is light"""
        try:
            hex_color = hex_color.lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            # Calculate relative luminance
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return luminance > 0.5
        except:
            return False
    
    def _lighten_color(self, hex_color: str, amount: float = 0.3) -> str:
        """Lighten a hex color"""
        try:
            hex_color = hex_color.lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            # Lighten by blending with white
            r = int(r + (255 - r) * amount)
            g = int(g + (255 - g) * amount)
            b = int(b + (255 - b) * amount)
            
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return hex_color
    
    def _darken_color(self, hex_color: str, amount: float = 0.3) -> str:
        """Darken a hex color"""
        try:
            hex_color = hex_color.lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            # Darken by reducing values
            r = int(r * (1 - amount))
            g = int(g * (1 - amount))
            b = int(b * (1 - amount))
            
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return hex_color


def get_extractor():
    return ColorExtractor()