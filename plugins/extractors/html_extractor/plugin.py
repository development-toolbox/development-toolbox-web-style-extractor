"""
HTML structure and DOM analysis plugin
"""
from plugins.base_plugin import BaseExtractor
from typing import Dict, Any


class HTMLExtractor(BaseExtractor):
    @property
    def name(self):
        return "html_extractor"
    
    @property
    def description(self):
        return "Extracts HTML structure and DOM information"
    
    def extract(self, soup, driver, url: str) -> Dict[str, Any]:
        """Extract HTML structure and metadata"""
        
        return {
            'title': self._get_title(soup),
            'meta_description': self._get_meta_description(soup),
            'meta_keywords': self._get_meta_keywords(soup),
            'open_graph': self._get_open_graph_data(soup),
            'headings': self._extract_headings(soup),
            'dom_structure': self._analyze_dom_structure(soup),
            'semantic_elements': self._get_semantic_elements(soup),
            'forms': self._analyze_forms(soup),
            'media': self._analyze_media(soup)
        }
    
    def _get_title(self, soup) -> str:
        """Get page title"""
        title_tag = soup.find('title')
        return title_tag.string.strip() if title_tag and title_tag.string else ""
    
    def _get_meta_description(self, soup) -> str:
        """Get meta description"""
        meta = soup.find('meta', attrs={'name': 'description'})
        if not meta:
            meta = soup.find('meta', attrs={'property': 'og:description'})
        return meta.get('content', '').strip() if meta else ""
    
    def _get_meta_keywords(self, soup) -> str:
        """Get meta keywords"""
        meta = soup.find('meta', attrs={'name': 'keywords'})
        return meta.get('content', '').strip() if meta else ""
    
    def _get_open_graph_data(self, soup) -> Dict[str, str]:
        """Extract Open Graph metadata"""
        og_data = {}
        og_tags = soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('og:')})
        
        for tag in og_tags:
            prop = tag.get('property', '')
            content = tag.get('content', '')
            if prop and content:
                og_data[prop] = content
        
        return og_data
    
    def _extract_headings(self, soup) -> Dict[str, list]:
        """Extract all headings with their text content"""
        headings = {}
        for level in range(1, 7):
            h_tags = soup.find_all(f'h{level}')
            headings[f'h{level}'] = [
                {
                    'text': h.get_text().strip(),
                    'id': h.get('id', ''),
                    'class': h.get('class', [])
                }
                for h in h_tags if h.get_text().strip()
            ]
        
        # Create hierarchy
        headings['hierarchy'] = self._build_heading_hierarchy(soup)
        return headings
    
    def _build_heading_hierarchy(self, soup) -> list:
        """Build hierarchical structure of headings"""
        hierarchy = []
        current_stack = []
        
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(heading.name[1])
            text = heading.get_text().strip()
            
            if not text:
                continue
            
            # Pop from stack until we find the right parent level
            while current_stack and current_stack[-1]['level'] >= level:
                current_stack.pop()
            
            heading_data = {
                'level': level,
                'text': text,
                'id': heading.get('id', ''),
                'children': []
            }
            
            if current_stack:
                current_stack[-1]['children'].append(heading_data)
            else:
                hierarchy.append(heading_data)
            
            current_stack.append(heading_data)
        
        return hierarchy
    
    def _analyze_dom_structure(self, soup) -> Dict[str, Any]:
        """Analyze DOM structure and patterns"""
        all_elements = soup.find_all()
        
        # Collect all classes and IDs
        classes = set()
        ids = set()
        
        for element in all_elements:
            if element.get('class'):
                classes.update(element['class'])
            if element.get('id'):
                ids.add(element['id'])
        
        # Count elements by tag
        tag_counts = {}
        for element in all_elements:
            tag = element.name
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Find repeated patterns (common class names)
        common_patterns = self._find_common_patterns(list(classes))
        
        return {
            'total_elements': len(all_elements),
            'unique_classes': list(classes)[:50],  # Limit to avoid huge data
            'unique_ids': list(ids)[:50],
            'class_count': len(classes),
            'id_count': len(ids),
            'tag_distribution': dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20]),
            'common_patterns': common_patterns
        }
    
    def _find_common_patterns(self, classes: list) -> list:
        """Find common patterns in class names"""
        patterns = {}
        
        for cls in classes:
            # Look for common prefixes
            parts = cls.split('-')
            if len(parts) > 1:
                prefix = parts[0]
                patterns[prefix] = patterns.get(prefix, 0) + 1
        
        # Return most common patterns
        return [pattern for pattern, count in 
                sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:10]]
    
    def _get_semantic_elements(self, soup) -> Dict[str, int]:
        """Count semantic HTML5 elements"""
        semantic_tags = [
            'header', 'nav', 'main', 'section', 'article', 'aside', 'footer',
            'figure', 'figcaption', 'time', 'mark', 'details', 'summary'
        ]
        
        semantic_count = {}
        for tag in semantic_tags:
            elements = soup.find_all(tag)
            if elements:
                semantic_count[tag] = len(elements)
        
        return semantic_count
    
    def _analyze_forms(self, soup) -> Dict[str, Any]:
        """Analyze form elements"""
        forms = soup.find_all('form')
        
        form_data = {
            'form_count': len(forms),
            'forms': []
        }
        
        for i, form in enumerate(forms[:5]):  # Limit to 5 forms
            inputs = form.find_all(['input', 'select', 'textarea', 'button'])
            
            input_types = {}
            for inp in inputs:
                inp_type = inp.get('type', inp.name)
                input_types[inp_type] = input_types.get(inp_type, 0) + 1
            
            form_data['forms'].append({
                'method': form.get('method', 'GET').upper(),
                'action': form.get('action', ''),
                'input_count': len(inputs),
                'input_types': input_types,
                'has_validation': bool(form.find_all(attrs={'required': True}))
            })
        
        return form_data
    
    def _analyze_media(self, soup) -> Dict[str, Any]:
        """Analyze media elements"""
        images = soup.find_all('img')
        videos = soup.find_all('video')
        audios = soup.find_all('audio')
        
        # Analyze image attributes
        img_analysis = {
            'total': len(images),
            'with_alt': len([img for img in images if img.get('alt')]),
            'with_loading_lazy': len([img for img in images if img.get('loading') == 'lazy']),
            'formats': self._get_image_formats(images)
        }
        
        return {
            'images': img_analysis,
            'videos': len(videos),
            'audios': len(audios),
            'has_responsive_images': bool(soup.find_all('picture')) or bool(soup.find_all('img', srcset=True))
        }
    
    def _get_image_formats(self, images) -> Dict[str, int]:
        """Analyze image formats from src attributes"""
        formats = {}
        
        for img in images[:20]:  # Limit analysis
            src = img.get('src', '')
            if '.' in src:
                ext = src.split('.')[-1].split('?')[0].lower()
                if ext in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp', 'avif']:
                    formats[ext] = formats.get(ext, 0) + 1
        
        return formats


def get_extractor():
    return HTMLExtractor()