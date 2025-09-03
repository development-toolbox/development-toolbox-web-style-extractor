"""
CSS parsing and analysis plugin
"""
import re
import logging
import tinycss2
import requests
from urllib.parse import urljoin
from plugins.base_plugin import BaseExtractor
from typing import List, Dict, Any


class CSSExtractor(BaseExtractor):
    @property
    def name(self):
        return "css_extractor"
    
    @property
    def description(self):
        return "Extracts and analyzes CSS rules and properties"
    
    def extract(self, soup, driver, url: str) -> Dict[str, Any]:
        """Extract CSS rules, selectors, and properties"""
        
        # Get all CSS text from the page
        css_text = self._get_all_css_text(soup, url)
        
        # Extract CSS rules and selectors
        css_rules = self._extract_css_rules(css_text)
        
        # Extract custom properties (CSS variables)
        custom_properties = self._extract_css_custom_properties(css_text)
        
        # Detect modern CSS features
        modern_features = self._detect_modern_css_features(css_text)
        
        # Analyze CSS architecture
        css_architecture = self._analyze_css_architecture(css_text, soup)
        
        # Extract media queries
        media_queries = self._extract_media_queries(css_text)
        
        return {
            'css_text': css_text[:10000],  # First 10k characters for reference
            'css_rules': css_rules,
            'custom_properties': custom_properties,
            'modern_features': modern_features,
            'css_architecture': css_architecture,
            'media_queries': media_queries,
            'total_css_size': len(css_text),
            'rule_count': len(css_rules.get('selectors', []))
        }
    
    def _get_all_css_text(self, soup, url: str) -> str:
        """Extract all CSS text from page"""
        css_text = ""
        
        # Extract inline styles
        inline_styles = []
        for element in soup.find_all(style=True):
            style_content = element.get('style', '')
            if style_content:
                inline_styles.append(style_content)
        
        if inline_styles:
            css_text += "/* Inline Styles */\n" + '\n'.join(inline_styles) + '\n\n'
        
        # Extract style tags
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                css_text += f"/* Style Tag */\n{style_tag.string}\n\n"
        
        # Extract external stylesheets
        for link in soup.find_all('link', rel='stylesheet')[:10]:  # Limit to 10 stylesheets
            href = link.get('href')
            if href:
                try:
                    if not href.startswith(('http', '//')):
                        href = urljoin(url, href)
                    elif href.startswith('//'):
                        href = f"https:{href}"
                    
                    response = requests.get(href, timeout=10)
                    response.raise_for_status()
                    css_text += f"/* External: {href} */\n{response.text}\n\n"
                except Exception as e:
                    logging.debug(f"Could not fetch CSS from {href}: {e}")
        
        return css_text
    
    def _extract_css_rules(self, css_text: str) -> Dict[str, Any]:
        """Extract CSS rules and selectors"""
        rules_data = {
            'selectors': [],
            'properties': {},
            'at_rules': [],
            'selector_types': {}
        }
        
        try:
            # Use tinycss2 for proper parsing
            rules = tinycss2.parse_stylesheet(css_text)
            
            for rule in rules:
                if rule.type == 'qualified-rule':
                    # Extract selector
                    selector = tinycss2.serialize(rule.prelude).strip()
                    rules_data['selectors'].append(selector)
                    
                    # Analyze selector type
                    self._categorize_selector(selector, rules_data['selector_types'])
                    
                    # Extract properties from declarations
                    declarations = tinycss2.parse_declaration_list(rule.content)
                    for declaration in declarations:
                        if declaration.type == 'declaration':
                            prop_name = declaration.name
                            prop_value = tinycss2.serialize(declaration.value).strip()
                            
                            if prop_name not in rules_data['properties']:
                                rules_data['properties'][prop_name] = []
                            rules_data['properties'][prop_name].append(prop_value)
                
                elif rule.type == 'at-rule':
                    rules_data['at_rules'].append({
                        'type': rule.at_keyword,
                        'cssText': tinycss2.serialize([rule])
                    })
        
        except Exception as e:
            logging.debug(f"tinycss2 parsing failed, using regex: {e}")
            # Fallback to regex parsing
            rules_data = self._extract_css_rules_regex(css_text)
        
        # Count property usage
        rules_data['property_usage'] = {
            prop: len(values) for prop, values in rules_data['properties'].items()
        }
        
        return rules_data
    
    def _extract_css_rules_regex(self, css_text: str) -> Dict[str, Any]:
        """Fallback CSS rule extraction using regex"""
        rules_data = {
            'selectors': [],
            'properties': {},
            'at_rules': [],
            'selector_types': {}
        }
        
        # Extract CSS rules (selector { declarations })
        rule_pattern = r'([^{}]+)\s*\{([^{}]*)\}'
        matches = re.findall(rule_pattern, css_text)
        
        for selector_part, declarations_part in matches:
            selector = selector_part.strip()
            if selector and not selector.startswith('@'):
                rules_data['selectors'].append(selector)
                self._categorize_selector(selector, rules_data['selector_types'])
                
                # Extract properties from declarations
                prop_pattern = r'([a-zA-Z-]+)\s*:\s*([^;]+)'
                props = re.findall(prop_pattern, declarations_part)
                
                for prop_name, prop_value in props:
                    prop_name = prop_name.strip()
                    prop_value = prop_value.strip()
                    
                    if prop_name not in rules_data['properties']:
                        rules_data['properties'][prop_name] = []
                    rules_data['properties'][prop_name].append(prop_value)
        
        return rules_data
    
    def _categorize_selector(self, selector: str, selector_types: Dict[str, int]):
        """Categorize CSS selector types"""
        if selector.startswith('#'):
            selector_types['id'] = selector_types.get('id', 0) + 1
        elif selector.startswith('.'):
            selector_types['class'] = selector_types.get('class', 0) + 1
        elif selector.startswith('@'):
            selector_types['at_rule'] = selector_types.get('at_rule', 0) + 1
        elif ':' in selector:
            selector_types['pseudo'] = selector_types.get('pseudo', 0) + 1
        elif '[' in selector:
            selector_types['attribute'] = selector_types.get('attribute', 0) + 1
        else:
            selector_types['element'] = selector_types.get('element', 0) + 1
    
    
    def _extract_css_custom_properties(self, css_text: str) -> Dict[str, str]:
        """Extract CSS custom properties (CSS variables)"""
        custom_props = {}
        
        # Pattern to match CSS custom properties: --property-name: value;
        prop_pattern = r'--([a-zA-Z0-9-_]+)\s*:\s*([^;}]+)'
        matches = re.findall(prop_pattern, css_text)
        
        for prop_name, prop_value in matches:
            # Clean up the value
            value = prop_value.strip().rstrip(';')
            custom_props[f'--{prop_name}'] = value
        
        return custom_props
    
    def _detect_modern_css_features(self, css_text: str) -> Dict[str, List[str]]:
        """Detect modern CSS features like container queries, nesting, etc."""
        features = {
            'container_queries': [],
            'css_nesting': [],
            'has_selectors': [],
            'custom_properties': [],
            'fluid_typography': [],
            'color_functions': [],
            'grid_areas': [],
            'logical_properties': []
        }
        
        # Detect container queries
        container_pattern = r'@container[^{]*\{[^{}]*\}'
        features['container_queries'] = re.findall(container_pattern, css_text)
        
        # Detect CSS nesting (& selector)
        nesting_pattern = r'&[^{]*\{[^{}]*\}'
        features['css_nesting'] = re.findall(nesting_pattern, css_text)
        
        # Detect :has() selectors
        has_pattern = r':has\([^)]*\)'
        features['has_selectors'] = re.findall(has_pattern, css_text)
        
        # Detect custom properties usage
        custom_prop_usage = r'var\(--[^)]+\)'
        features['custom_properties'] = re.findall(custom_prop_usage, css_text)
        
        # Detect fluid typography (clamp, min, max functions)
        fluid_pattern = r'(?:clamp|min|max)\([^)]+\)'
        features['fluid_typography'] = re.findall(fluid_pattern, css_text)
        
        # Detect modern color functions
        color_function_pattern = r'(?:oklch|lab|lch|color-mix|color)\([^)]+\)'
        features['color_functions'] = re.findall(color_function_pattern, css_text)
        
        # Detect CSS Grid areas
        grid_area_pattern = r'grid-template-areas\s*:\s*[^;]+'
        features['grid_areas'] = re.findall(grid_area_pattern, css_text)
        
        # Detect logical properties
        logical_props = ['margin-inline', 'margin-block', 'padding-inline', 'padding-block', 
                        'border-inline', 'border-block', 'inset-inline', 'inset-block']
        for prop in logical_props:
            if prop in css_text:
                features['logical_properties'].append(prop)
        
        # Remove empty features
        return {k: v for k, v in features.items() if v}
    
    def _analyze_css_architecture(self, css_text: str, soup) -> Dict[str, Any]:
        """Analyze CSS architecture and methodology patterns"""
        architecture = {
            'methodology': self._detect_css_methodology(css_text),
            'naming_patterns': self._analyze_naming_patterns(css_text),
            'organization': self._analyze_css_organization(css_text),
            'complexity': self._calculate_css_complexity(css_text)
        }
        
        return architecture
    
    def _detect_css_methodology(self, css_text: str) -> List[str]:
        """Detect CSS methodologies (BEM, OOCSS, SMACSS, etc.)"""
        methodologies = []
        
        # BEM detection (block__element--modifier)
        bem_pattern = r'\.[\w-]+__[\w-]+(?:--[\w-]+)?'
        if re.search(bem_pattern, css_text):
            methodologies.append('BEM')
        
        # OOCSS detection (object-oriented patterns)
        oocss_patterns = ['media', 'flag', 'nav', 'btn', 'card']
        if any(f'.{pattern}' in css_text for pattern in oocss_patterns):
            methodologies.append('OOCSS')
        
        # Utility-first detection (Tailwind-like)
        utility_patterns = [r'\.text-\w+', r'\.bg-\w+', r'\.p-\d+', r'\.m-\d+', r'\.w-\d+']
        if any(re.search(pattern, css_text) for pattern in utility_patterns):
            methodologies.append('Utility-First')
        
        return methodologies
    
    def _analyze_naming_patterns(self, css_text: str) -> Dict[str, int]:
        """Analyze CSS class naming patterns"""
        patterns = {
            'camelCase': 0,
            'kebab-case': 0,
            'snake_case': 0,
            'PascalCase': 0
        }
        
        # Extract all class names
        class_pattern = r'\.([a-zA-Z][\w\-_]*)'
        classes = re.findall(class_pattern, css_text)
        
        for class_name in classes:
            if '_' in class_name:
                patterns['snake_case'] += 1
            elif '-' in class_name:
                patterns['kebab-case'] += 1
            elif class_name[0].isupper():
                patterns['PascalCase'] += 1
            elif any(c.isupper() for c in class_name[1:]):
                patterns['camelCase'] += 1
        
        return patterns
    
    def _analyze_css_organization(self, css_text: str) -> Dict[str, Any]:
        """Analyze how CSS is organized"""
        organization = {
            'has_comments': bool(re.search(r'/\*.*?\*/', css_text, re.DOTALL)),
            'has_sections': bool(re.search(r'/\*\s*={3,}.*?={3,}\s*\*/', css_text)),
            'import_count': len(re.findall(r'@import', css_text)),
            'media_query_count': len(re.findall(r'@media', css_text))
        }
        
        return organization
    
    def _calculate_css_complexity(self, css_text: str) -> Dict[str, Any]:
        """Calculate CSS complexity metrics"""
        # Count selectors
        selector_count = len(re.findall(r'[^{}]+\{', css_text))
        
        # Count properties
        property_count = len(re.findall(r'[a-zA-Z-]+\s*:', css_text))
        
        # Calculate average selector complexity (number of parts)
        selectors = re.findall(r'([^{}]+)\{', css_text)
        avg_selector_parts = 0
        if selectors:
            total_parts = sum(len(selector.split()) for selector in selectors)
            avg_selector_parts = total_parts / len(selectors)
        
        return {
            'selector_count': selector_count,
            'property_count': property_count,
            'avg_selector_complexity': round(avg_selector_parts, 2),
            'lines_of_css': len(css_text.split('\n'))
        }
    
    def _extract_media_queries(self, css_text: str) -> List[Dict[str, str]]:
        """Extract media queries and their conditions"""
        media_queries = []
        
        # Pattern to match @media rules
        media_pattern = r'@media\s+([^{]+)\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
        matches = re.findall(media_pattern, css_text, re.DOTALL)
        
        for condition, content in matches:
            media_queries.append({
                'condition': condition.strip(),
                'content': content.strip()[:500],  # Limit content length
                'rules_count': len(re.findall(r'\{[^{}]*\}', content))
            })
        
        return media_queries[:10]  # Limit to 10 media queries


def get_extractor():
    return CSSExtractor()