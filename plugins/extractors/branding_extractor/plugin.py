"""
Branding and logo extraction plugin for BookStack themes
"""
import requests
import logging
from urllib.parse import urljoin, urlparse
from plugins.base_plugin import BaseExtractor
from typing import Dict, Any


class BrandingExtractor(BaseExtractor):
    @property
    def name(self):
        return "branding_extractor"
    
    @property
    def description(self):
        return "Extracts logos, favicons, and brand elements for theme generation"
    
    def extract(self, soup, driver, url: str) -> Dict[str, Any]:
        """Extract branding assets and information"""
        branding = {}
        
        # Extract logo
        logo_url = self._extract_logo(soup, url)
        if logo_url:
            branding['logo_url'] = logo_url
        
        # Extract favicon
        favicon_url = self._extract_favicon(soup, url)
        if favicon_url:
            branding['favicon_url'] = favicon_url
        
        # Extract brand colors from meta/CSS
        brand_colors = self._extract_brand_colors(soup)
        if brand_colors:
            branding['brand_colors'] = brand_colors
        
        # Extract organization name
        org_name = self._extract_organization_name(soup)
        if org_name:
            branding['organization'] = org_name
        
        # Extract theme color (from meta tags)
        theme_color = self._extract_theme_color(soup)
        if theme_color:
            branding['theme_color'] = theme_color
        
        # Extract Apple touch icons
        apple_icons = self._extract_apple_touch_icons(soup, url)
        if apple_icons:
            branding['apple_touch_icons'] = apple_icons
        
        return branding
    
    def _extract_logo(self, soup, base_url: str) -> str:
        """Extract organization logo using various selectors"""
        logo_selectors = [
            'img[class*="logo"]',
            'img[id*="logo"]', 
            'img[alt*="logo"]',
            'img[src*="logo"]',
            '.header img',
            '.navbar img',
            '.brand img',
            '.logo img',
            'header img:first-of-type',
            '.navbar-brand img',
            '.site-logo img',
            '.brand-logo img'
        ]
        
        for selector in logo_selectors:
            logos = soup.select(selector)
            for logo in logos:
                src = logo.get('src')
                if src and self._is_likely_logo(logo, src):
                    logo_url = urljoin(base_url, src)
                    if self._validate_image_url(logo_url):
                        return logo_url
        
        # Try to find logo in SVG elements
        svg_logos = soup.find_all('svg', class_=lambda x: x and 'logo' in ' '.join(x).lower())
        if svg_logos:
            # For SVG logos, we'd need to convert them or note their presence
            return f"{base_url}#svg-logo-found"
        
        return None
    
    def _extract_favicon(self, soup, base_url: str) -> str:
        """Extract favicon"""
        favicon_selectors = [
            'link[rel="icon"]',
            'link[rel="shortcut icon"]', 
            'link[rel="apple-touch-icon"]',
            'link[rel="favicon"]'
        ]
        
        for selector in favicon_selectors:
            favicon = soup.select_one(selector)
            if favicon and favicon.get('href'):
                href = favicon['href']
                favicon_url = urljoin(base_url, href)
                if self._validate_image_url(favicon_url):
                    return favicon_url
        
        # Fallback to default favicon location
        default_favicon = urljoin(base_url, '/favicon.ico')
        if self._validate_image_url(default_favicon):
            return default_favicon
        
        return None
    
    def _extract_brand_colors(self, soup) -> list:
        """Extract brand colors from CSS custom properties and meta tags"""
        brand_colors = []
        
        # Check for theme-color meta tag
        theme_color = soup.find('meta', {'name': 'theme-color'})
        if theme_color and theme_color.get('content'):
            brand_colors.append(theme_color['content'])
        
        # Look for CSS custom properties that might be brand colors
        style_tags = soup.find_all('style')
        for style in style_tags:
            if style.string:
                lines = style.string.split('\n')
                for line in lines:
                    if '--' in line and any(keyword in line.lower() 
                                         for keyword in ['color', 'brand', 'primary', 'theme']):
                        # Extract color value
                        if ':' in line:
                            color_value = line.split(':')[1].strip().rstrip(';')
                            if (color_value.startswith('#') or 
                                color_value.startswith('rgb') or 
                                color_value.startswith('hsl')):
                                brand_colors.append(color_value)
        
        return brand_colors[:5]  # Limit to 5 colors
    
    def _extract_organization_name(self, soup) -> str:
        """Extract organization/company name"""
        # Try multiple sources for organization name
        sources = [
            soup.find('meta', {'property': 'og:site_name'}),
            soup.find('meta', {'name': 'application-name'}),
            soup.find('meta', {'name': 'apple-mobile-web-app-title'}),
            soup.find('meta', {'property': 'og:title'}),
        ]
        
        for source in sources:
            if source:
                content = source.get('content', '').strip()
                if content and len(content) > 0:
                    return content
        
        # Try title tag as last resort
        title_tag = soup.find('title')
        if title_tag and title_tag.string:
            title = title_tag.string.strip()
            # Remove common suffixes
            for suffix in [' - Home', ' | Home', ' - Official Site', ' | Official Site']:
                if title.endswith(suffix):
                    title = title[:-len(suffix)]
            return title
        
        return None
    
    def _extract_theme_color(self, soup) -> str:
        """Extract theme color from meta tags"""
        theme_color = soup.find('meta', {'name': 'theme-color'})
        if theme_color:
            return theme_color.get('content', '')
        
        # Check for MSApplication tile color
        ms_tile_color = soup.find('meta', {'name': 'msapplication-TileColor'})
        if ms_tile_color:
            return ms_tile_color.get('content', '')
        
        return None
    
    def _extract_apple_touch_icons(self, soup, base_url: str) -> list:
        """Extract Apple touch icons of various sizes"""
        apple_icons = []
        
        apple_icon_links = soup.find_all('link', rel=lambda x: x and 'apple-touch-icon' in x)
        
        for link in apple_icon_links:
            href = link.get('href')
            sizes = link.get('sizes', '')
            
            if href:
                icon_url = urljoin(base_url, href)
                if self._validate_image_url(icon_url):
                    apple_icons.append({
                        'url': icon_url,
                        'sizes': sizes,
                        'type': 'apple-touch-icon'
                    })
        
        return apple_icons
    
    def _is_likely_logo(self, img_element, img_src: str) -> bool:
        """Heuristic to determine if image is likely a logo"""
        # Check image attributes
        attrs_text = ' '.join([
            str(img_element.get('class', [])),
            str(img_element.get('id', '')),
            str(img_element.get('alt', '')),
            str(img_src)
        ]).lower()
        
        logo_indicators = ['logo', 'brand', 'header', 'nav']
        non_logo_indicators = ['banner', 'hero', 'background', 'avatar', 'profile']
        
        # Positive indicators
        logo_score = sum(2 if indicator in attrs_text else 0 for indicator in logo_indicators)
        
        # Negative indicators  
        non_logo_score = sum(1 if indicator in attrs_text else 0 for indicator in non_logo_indicators)
        
        # Size-based heuristics (if available)
        width = img_element.get('width')
        height = img_element.get('height')
        
        if width and height:
            try:
                w, h = int(width), int(height)
                # Logos are typically not too large and have reasonable aspect ratios
                if w > 500 or h > 500:  # Too large for a logo
                    non_logo_score += 2
                elif 20 <= w <= 300 and 20 <= h <= 150:  # Good logo size range
                    logo_score += 1
            except ValueError:
                pass
        
        # URL-based heuristics
        url_lower = img_src.lower()
        if any(x in url_lower for x in ['logo', 'brand']):
            logo_score += 3
        
        if any(x in url_lower for x in ['banner', 'hero', 'bg', 'background']):
            non_logo_score += 2
        
        return logo_score > non_logo_score
    
    def _validate_image_url(self, url: str) -> bool:
        """Validate that URL points to an accessible image"""
        try:
            # Parse URL to check if it looks valid
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Check for common image extensions
            path_lower = parsed.path.lower()
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp']
            
            # If it has an image extension, consider it valid
            if any(path_lower.endswith(ext) for ext in image_extensions):
                return True
            
            # For URLs without extensions, try a HEAD request (but don't fail if it doesn't work)
            try:
                response = requests.head(url, timeout=5, allow_redirects=True)
                content_type = response.headers.get('content-type', '').lower()
                return content_type.startswith('image/')
            except:
                # If we can't verify, assume it might be valid
                return True
                
        except Exception:
            return False
        
        return False


def get_extractor():
    return BrandingExtractor()